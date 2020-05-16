from string import Template
from Config import *

method = "SubmitOrder"

order = """
<Order>
  <ExtraInfo>REF 1234</ExtraInfo>
  <Instructions>Testvia Websiervice</Instructions>
  <TransferDate>2019-06-25</TransferDate>
  <Lines> 
    <Line>
            <ProductCode>VERLICHT</ProductCode>
            <Name>WERFLAMP VERLICHTING 10W (OPLAADBAAR)</Name>
            <Quantity>1</Quantity>
            <GrossPrice>0</GrossPrice>
            <NetPrice>0</NetPrice>
            <GrossLineTotal>0</GrossLineTotal>
            <NetLineTotal>0</NetLineTotal>
    </Line>
    <Line>
            <ProductCode>UHOM160</ProductCode>
            <Quantity>4.2</Quantity>
    </Line>
  </Lines>

  <ShippingMethod>Delivery</ShippingMethod>
  <PickupLocation>Tielt</PickupLocation>

  <DeliveryAddressName>John Doe</DeliveryAddressName>
  <DeliveryAddressName2></DeliveryAddressName2>
  <DeliveryAddressStreet>Kerkstraat 101</DeliveryAddressStreet>
  <DeliveryAddressStreet2></DeliveryAddressStreet2>
  <DeliveryAddressZip>1040</DeliveryAddressZip>
  <DeliveryAddressCity>Brussel</DeliveryAddressCity>
  <DeliveryAddressEmail>johnd@brussels.be</DeliveryAddressEmail>
  <DeliveryAddressCountryCode>BE</DeliveryAddressCountryCode>

  <ContactFirstName>Jane</ContactFirstName>
  <ContactLastName>Doe</ContactLastName>
  <ContactMiddleName></ContactMiddleName>
  <ContactGender>Female</ContactGender>
  <ContactEmail>janed@gmail.com</ContactEmail>
  <ContactEmail2>doe.jane@yahoo.com</ContactEmail2>
  <ContactFax></ContactFax>
  <ContactPhone>555-121215</ContactPhone>
  <ContactMobile>555-454544</ContactMobile>
  <ContactTitle>Account Manager</ContactTitle>

  <AccessibleForTrailer>true</AccessibleForTrailer>
  <CraneAvailable>false</CraneAvailable>
  <ForkliftAvailable>false</ForkliftAvailable>

</Order>
"""

messagetemplate = Template(r"""<?xml version="1.0" encoding="utf-8"?>
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soapenv:Body>
      <$method xmlns="http://www.deschacht.eu/">
         <Login>$login</Login>
         <Password>$password</Password>
         $order
      </$method>
   </soapenv:Body>
</soapenv:Envelope>""")


body = messagetemplate.substitute(login = login, password = password, order = order, method = method)
result = fire_post_request(url1, body, 60, method)

print(result)
