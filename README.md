pyUspsLib
=========

NOTES
-------------------------
Requires Requests
USPS requires you run tests with their data before you can get production permissions. These tests are included.


Features
-------------------------
This package allows you to get data from USPS. It currently supports address verification, shipping pricing, and package tracking.


Installation
-------------------------

EASY :

	pip install pyuspslib

from github :

	pip install https://github.com/luxnovalabs/pyUspsLib/zipball/master


Running the USPS test data:
	
	from pyuspslib import tests
	user_id = 'my_usps_user_id'
	tests.run_all_tests(user_id)

	shipping domestic and international shipping pricing will fail.
	Despite the docuementation, you don't have access yet


After running the tests, give USPS a call. The instructions say to email, but I gave up after waiting 72 hours. The phone call took minutes.


BASIC USAGE
==================

	from pyuspslib.lib import USPS
	user_id = 'my_usps_user_id'

	usps = USPS(user_id)


all methods return a dictionary with "value", "error", and "xml" keys


	#find city and state for a given zipcode
	response = usps.loopkup_city_state('84115')
	print response['value'] # returns {'city':'value', 'state':'value'}
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree


	#returns a zipcode for the address information given
	response = usps.lookup_zipcode({'Address2':'244 Edison', 'City':'Salt Lake City', 'State':'UT'})
	print response['value'] # returns 84111
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree


	#returns a zipcode for the address information given
	response = usps.verify_address({'Address2':'244 Edison', 'City':'Salt Lake City', 'State':'UT'})
	print response['value'] # returns 'valid' or None
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree


	#returns status of a packge id
	response = usps.track_package('EJ958083578US')
	print response['value'] # returns 'valid' or None
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree



INTERMEDIATE USAGE
==================

USPS has specific fields that must be sent. With shipping prices, the structure gets a little complicated.

1) Start by copying the defaults.py file and creating a usps instance like this:

	from pyuspslib.lib import USPS
	import my_custom_defaults

	user_id = 'my_usps_user_id'

	usps = USPS(user_id, my_custom_defaults)

2) Take a look at the defaults file and change the origin zipcode

	USPS_MERCHANT_ORIGIN_ZIPCODE = 'your zipcode'

3) You should also set useful defaults for package defaults. Weight, size, and shape all affect the price. International pacakges need additonal information.

4) The methods provided are written to be simple, and pull the extra data needed from the defaults. If you need more control, see the advanced section.

	#returns price of domestic shipping
	#needs shipping_type and destination zipcode
	response = usps.price_domestic_shipping('PRIORITY','84111') 
	print response['value'] # returns a decimal price
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree


International shipping is more complicated. You're basically forced into advanced usage - which is still really simple.

USPS requires fields, even if empty. We'll pull the template from the defaults and stuff our values in the template.	

	from pyuspslib import defaults 

	#merge default data with new value
	package_data = defaults.USPS_DEFAULT_INTERNATIONAL_PACKAGE_DATA.update({'ValueOfContents':'50'})
	
	#returns a list of shipping options
	response = usps.price_international_shipping(package_data)
	print response['value'] # returns a set of shipping options
	print response['error'] # returns string from usps describing the error
	print response['xml'] # raw xml from python's xml.etree.ElementTree




ADVANCED USAGE
==================

The USPS library is written to provide some convenience, but also allow you to override everything. You've probably noticed that all methods return a dictionary with a 'xml' key. You can crawl that data as much as you like to get anything usps provides.

The methods, at first glance, allow limited data entry, however they have arguments with defaults you can override.

For example, if you are getting a domestic shipping estimate and the shipping type and zipcode are not enough, look at the methods  in lib.USPS to see what you can override.

Instead of this:
	
	response = usps.price_domestic_shipping('PRIORITY','84111')

you can call this:
	
	response usps.price_domestic_shipping(shipping_type, destination_zipcode, package_data=None, api='RateV4')

If package_data = None, the method pulls in the defaults.USPS_DEFAULT_DOMESTIC_PACKAGE_DATA and uses that. For custom data, bring in your own instance and override the values.
	
	package_data = defaults.USPS_DEFAULT_INTERNATIONAL_PACKAGE_DATA.update({'ValueOfContents':'50'})

and pass your package_data into the method



If the data structure changes on the USPS end, you can pass custom xml templates into the USPS constructor.



