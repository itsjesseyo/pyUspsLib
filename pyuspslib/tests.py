import requests
import defaults

class address_test():

	def __init__(self, user_id, base_url):
		self.request = None
		self.user_id = user_id
		self.base_url = base_url

	def usps_address_verify(self, user_id, base_url, api='Verify'):
		url = '%s?API=%s&XML=<AddressValidateRequest USERID="%s">\
			<Address>\
				<Address1></Address1>\
				<Address2>6406 Ivy Lane</Address2>\
				<City>Greenbelt</City>\
				<State>MD</State> \
				<Zip5></Zip5>\
				<Zip4></Zip4>\
			</Address>\
		</AddressValidateRequest>' % (base_url, api, user_id)
		self.request = requests.get(url)

	def usps_zipcode_lookup(self, user_id, base_url, api='ZipCodeLookup'):
		url = '%s?API=%s&XML=<ZipCodeLookupRequest USERID="%s">\
			<Address>\
				<Address1></Address1>\
				<Address2>6406 Ivy Lane</Address2>\
				<City>Greenbelt</City>\
				<State>MD</State> \
			</Address>\
		</ZipCodeLookupRequest>' % (base_url, api, user_id)
		self.request = requests.get(url)


	def usps_city_state_lookup(self, user_id, base_url, api='CityStateLookup'):
		url = '%s?API=%s&XML=<CityStateLookupRequest USERID="%s">\
				<ZipCode ID= "0">\
					<Zip5>90210</Zip5>\
				</ZipCode>\
		</CityStateLookupRequest>' % (base_url, api, user_id)
		self.request = requests.get(url)

	def run_tests(self):
		self.usps_address_verify(self.user_id, self.base_url)
		print 'ADDRESS_VERIFY : %s' % self.request.text
		self.usps_zipcode_lookup(self.user_id, self.base_url)
		print 'ZIPCODE_LOOKUP : %s' % self.request.text
		self.usps_city_state_lookup(self.user_id, self.base_url)
		print 'CITY_STATE_LOOKUP : %s' % self.request.text


class tracking_test():

	def __init__(self, user_id, base_url):
		self.request = None
		self.user_id = user_id
		self.base_url = base_url

	def tracking_test(self, user_id, base_url, api='TrackV2'):
		url = '%s?API=%s&XML=<TrackRequest USERID="%s">\
			<TrackID ID="EJ958083578US"></TrackID>\
		</TrackRequest>' % (base_url, api, user_id)
		self.request = requests.get(url)

	def run_tests(self):
		self.tracking_test(self.user_id, self.base_url)
		print 'TACKING_TEST : %s' % self.request.text


class shipping_test():

	def __init__(self, user_id, base_url):
		self.request = None
		self.base_url = base_url
		self.user_id = user_id

	def domestic_shipping_test(self, user_id, base_url, api='RateV4'):
		url = '%s?API=%s&XML=<RateV4Request USERID="%s" >\
			<Revision/>\
				<Package ID="1ST">\
					<Service>PRIORITY</Service>\
					<ZipOrigination>44106</ZipOrigination>\
					<ZipDestination>20770</ZipDestination>\
					<Pounds>1</Pounds>\
					<Ounces>8</Ounces>\
					<Container>NONRECTANGULAR</Container>\
					<Size>LARGE</Size>\
					<Width>15</Width>\
					<Length>30</Length>\
					<Height>15</Height>\
					<Girth>55</Girth>\
				</Package>\
			</RateV4Request>' % (base_url, api, user_id)
		self.request = requests.get(url)

	def inernational_shipping_test(self, user_id, base_url, api='IntlRateV2'):
		url = '%s?API=%s&XML=<IntlRateV2Request USERID="%s">\
			<Revision>2</Revision> \
				<Package>\
					<Pounds>69</Pounds>\
					<Ounces>0</Ounces> \
					<Machinable>True</Machinable>\
					<MailType>all</MailType>\
					<GXG>\
						<POBoxFlag>N</POBoxFlag>\
						<GiftFlag>N</GiftFlag>\
					</GXG>\
					<ValueOfContents>100.00</ValueOfContents>\
					<Country>canada</Country>\
					<Container>RECTANGULAR</Container>\
					<Size>Regular</Size>\
					<Width>10</Width>\
					<Length>10</Length>\
					<Height>11</Height>\
					<Girth></Girth>\
					<CommercialFlag>y</CommercialFlag>\
				</Package>\
			</IntlRateV2Request>' % (base_url, api, user_id)
		self.request = requests.get(url)

	def run_tests(self):
		self.domestic_shipping_test(self.user_id, self.base_url)
		print 'SHIPPING_TEST : %s' % self.request.text
		self.inernational_shipping_test(self.user_id, self.base_url)
		print 'INTERNATIONAL_TEST : %s' % self.request.text



def run_all_tests(user_id):

	address = address_test(user_id, defaults.USPS_TEST_URL)
	address.run_tests()

	tracking = tracking_test(user_id, defaults.USPS_TEST_URL)
	tracking.run_tests()

	shipping = shipping_test(user_id, defaults.USPS_TEST_URL)
	shipping.run_tests()









