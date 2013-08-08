USPS_USER_ID = 'my_user_id'
USPS_TESTMODE = False
USPS_TEST_URL = 'http://production.shippingapis.com/ShippingAPITest.dll'
USPS_PRODUCTION_URL = 'http://production.shippingapis.com/ShippingAPI.dll'
USPS_MERCHANT_ORIGIN_ZIPCODE = '84111'
USPS_BASE_SHIPPING_FEE = 0
USPS_SHIPPING_OPTIONS = {
    'Priority':
        {
            'Container':'Md Flat Rate Box',
            'Size':'Regular',
            'Ounces':'4',
            'Pounds':'0',
        },
    'Standard Post':
        {
            'Size':'Regular',
            'Machinable':'true',
            'Ounces':'4',
            'Pounds':'0',
        },
}