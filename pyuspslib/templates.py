domestic_shipping_template = '''<RateV4Request>
<Revision></Revision>
<Package ID="1ST">
<Service></Service>
<ZipOrigination></ZipOrigination>
<ZipDestination></ZipDestination>
<Pounds></Pounds>
<Ounces></Ounces>
<Container></Container>
<Size></Size>
<Width></Width>
<Length></Length>
<Height></Height>
<Girth></Girth>
</Package>
</RateV4Request>'''

international_shipping_template = '''<IntlRateV2Request>
<Revision>2</Revision>
<Package ID="1ST">
<Pounds></Pounds>
<Ounces></Ounces>
<Machinable></Machinable>
<MailType></MailType>
<GXG>
<POBoxFlag>N</POBoxFlag>
<GiftFlag>N</GiftFlag>
</GXG>
<ValueOfContents></ValueOfContents>
<Country></Country>
<Container></Container>
<Size></Size>
<Width></Width>
<Length></Length>
<Height></Height>
<Girth></Girth>
<CommercialFlag></CommercialFlag>
</Package>
</IntlRateV2Request>'''

address_template = '''<AddressValidateRequest>
<Address>
<Address1></Address1>
<Address2></Address2>
<City></City>
<State></State>
<Zip5></Zip5>
<Zip4></Zip4>
</Address>
</AddressValidateRequest>'''

zipcode_template = '''<ZipCodeLookupRequest>
<Address>
<Address1></Address1>
<Address2></Address2>
<City></City>
<State></State>
</Address>
</ZipCodeLookupRequest>'''

city_state_template = '''<CityStateLookupRequest>
<ZipCode ID="0">
<Zip5></Zip5>
</ZipCode>
</CityStateLookupRequest>'''

tracking_template = '''<TrackRequest>
<TrackID></TrackID>
</TrackRequest>'''
