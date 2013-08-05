USPS_USER_ID = 'my_user_id'
USPS_TESTMODE = False
USPS_TEST_URL = 'http://production.shippingapis.com/ShippingAPITest.dll'
USPS_PRODUCTION_URL = 'http://production.shippingapis.com/ShippingAPI.dll'
USPS_MERCHANT_ORIGIN_ZIPCODE = '84111'
USPS_BASE_SHIPPING_FEE = 0
USPS_DEFAULT_DOMESTIC_PACKAGE_DATA = {
		'Pounds':'1',
		'Ounces':'2',
		'Container':'NONRECTANGULAR',
		'Size':'LARGE',
		'Width':'15',
		'Length':'30',
		'Height':'15',
		'Girth':'55'
}
USPS_DEFAULT_INTERNATIONAL_PACKAGE_DATA = {
		'Pounds':'20',
		'Ounces':'2',
		'Container':'RECTANGULAR',
		'Size':'Regular',
		'Width':'10',
		'Length':'10',
		'Height':'10',
		'Machinable':'True',
		'MailType':'all',
		'Country':'canada',
		'CommercialFlag':'y'

}