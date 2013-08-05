import requests
import xml.etree.ElementTree as XML
from decimal import Decimal

import defaults, templates, tests


class USPS():

	def __init__(self, user_id=None, settings_file=defaults, templates=templates):
		self.request = None
		self.user_id = user_id if user_id else settings_file.USPS_USER_ID
		self.base_shipping_fee = settings_file.USPS_BASE_SHIPPING_FEE
		self.merchant_zipcode = settings_file.USPS_MERCHANT_ORIGIN_ZIPCODE
		self.base_url = settings_file.USPS_TEST_URL if settings_file.USPS_TESTMODE else settings_file.USPS_PRODUCTION_URL
		self.default_domestic_package_data = settings_file.USPS_DEFAULT_DOMESTIC_PACKAGE_DATA
		self.default_international_package_data = settings_file.USPS_DEFAULT_INTERNATIONAL_PACKAGE_DATA
		self.templates = templates

	##########################
	#  ADDRESS VERIFICATION  #
	##########################
	def verify_address(self, address_data={}, api='Verify'):
		#login info
		xml = XML.fromstring(self.templates.address_template)
		xml.set('USERID', self.user_id)
		#address bindings
		address = xml.find('Address')
		for key, value in address_data.iteritems():
			address.find(key).text = value
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		#error checking
		error = response_xml.find('.//Description')
		response = {
			'error':error.text if error is not None else None,
			'value':True if error is None else False,
			'xml':response_xml
		}
		return response

	def lookup_zipcode(self, address_data={}, api='ZipCodeLookup'):
		#login info
		xml = XML.fromstring(self.templates.zipcode_template)
		xml.set('USERID', self.user_id)
		#address bindings
		address = xml.find('Address')
		for key, value in address_data.iteritems():
			address.find(key).text = value
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		#error checking
		error = response_xml.find('.//Description')
		response = {
			'error':error.text if error is not None else None,
			'value':response_xml.find('.//Zip5').text if error is None else error.text,
			'xml':response_xml
		}
		return response
		

	def loopkup_city_state(self, zipcode, api='CityStateLookup'):
		#login info
		xml = XML.fromstring(self.templates.city_state_template)
		xml.set('USERID', self.user_id)
		#address bindings
		xml.find('.//Zip5').text = zipcode
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		#error checking
		error = response_xml.find('.//Description')
		city = response_xml.find('.//City').text if error is None else None
		state = response_xml.find('.//State').text if error is None else None
		response = {
			'error':error.text if error is not None else None,
			'value':{'city':city, 'state':state},
			'xml':response_xml
		}
		return response

	##########################
	#  	  SHIPPING PRICES    #
	##########################
	#dimensions.lbs, .ounces, .container_shape, .size, .width, .length, .height, .girth
	def price_domestic_shipping(self, shipping_type, destination_zipcode, package_data=None, api='RateV4'):
		details = package_data if package_data else self.default_domestic_package_data
		#login info
		xml = XML.fromstring(self.templates.domestic_shipping_template)
		xml.set('USERID', self.user_id)
		#package binding
		package = xml.find('Package')
		package.find('ZipOrigination').text = self.merchant_zipcode
		package.find('ZipDestination').text = destination_zipcode
		package.find('Service').text = shipping_type
		for key, value in details.iteritems():
			package.find(key).text = value
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		#error checking
		error = response_xml.find('.//Description')
		rate = Decimal(response_xml.find('.//Rate').text) if error is None else None
		response = {
			'error':error.text if error is not None else None,
			'value':rate,
			'xml':response_xml
		}
		return response

		
	def price_international_shipping(self, package_data, flags={}, api='IntlRateV2'):
		details = package_data if package_data else self.default_international_package_data
		#login info
		xml = XML.fromstring(self.templates.international_shipping_template)
		xml.set('USERID', self.user_id)
		#package data
		package = xml.find('Package')
		for key, value in details.iteritems():
			package.find(key).text = value
		#gifts and POBox
		gxg = package.find('GXG')
		for key, value in flags.iteritems():
			gxg.find(key).text = value
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		error = response_xml.find('.//Description')
		#returns multiple shipping options
		services = response_xml.find('Package').findall('Service')
		rates={}
		if error is None:
			for service in services:
				service_id = service.get('ID')
				Postage = service.find('Postage')
				CommercialPostage = service.find('CommercialPostage')
				SvcCommitments = service.find('SvcCommitments')
				SvcDescription = service.find('SvcDescription')
				rates[str(service_id)] = {
					'Postage': Decimal(Postage.text) if Postage is not None else None,
					'CommercialPostage':Decimal(CommercialPostage.text) if CommercialPostage is not None else None,
					'SvcCommitments':SvcCommitments.text if SvcCommitments is not None else None,
					'SvcDescription':SvcDescription.text if SvcDescription is not None else None,
				}
		response = {
			'error':error.text if error is not None else None,
			'value': rates,
			'xml':response_xml
		}
		return response
		


	###############
	#  TRACKING   #
	###############
	def track_package(self, tracking_id, api='TrackV2'):
		#login info
		xml = XML.fromstring(self.templates.tracking_template)
		xml.set('USERID', self.user_id)
		#tacking_id
		tracking_element = xml.find('TrackID')
		tracking_element.set('ID', tracking_id)
		#request
		self.request = requests.get('%s?API=%s&XML=%s' % (self.base_url, api, XML.tostring(xml)))
		response_xml = XML.fromstring(self.request.text)
		#error checking
		error = response_xml.find('.//Description')
		status = response_xml.find('.//TrackSummary')
		response = {
			'error':error.text if error is not None else None,
			'value': status.text if status is not None else None,
			'xml':response_xml
		}
		return response

######################
#  UTILITIES  #
######################
# def step_dictionary(xml, obj):
# 	for key, value in obj.iteritems():
# 		child = XML.SubElement(xml, key)
# 		if type(value) is dict:
# 			step_dictionary(child, value)
# 		else:
# 			child.text = value


# def dictionary_to_xml(obj, user_id, root_element):
# 	root = XML.Element(root_element)
# 	root.set('USERID', user_id)
# 	step_dictionary(root, obj)
# 	return root


def ounces_to_lbs(ounces):
	#returns object with lbs and ounces
	pass

def lbs_to_ounces(lbs):
	pass


#step 1 run all tests and then call usps and get production certified
#tests.run_all_tests(defaults.USPS_USER_ID)

#step 2 run these examples check the results
# response = usps.loopkup_city_state('84115')
# print response['status']

# response = usps.lookup_zipcode({'Address2':'244 Edison', 'City':'Salt Lake City', 'State':'UT'})
# print response['status']

# response = usps.verify_address({'Address2':'244 Edison', 'City':'Salt Lake City', 'State':'UT'})
# print response['status']

# response = usps.track_package('EJ958083578US')
# print response['status']

# response = usps.price_domestic_shipping('PRIORITY','84105')
# print response['rate']

# package_data = defaults.USPS_DEFAULT_INTERNATIONAL_PACKAGE_DATA.update({'ValueOfContents':'50'})
# response = usps.price_international_shipping(package_data)
# print len(response['services'])
