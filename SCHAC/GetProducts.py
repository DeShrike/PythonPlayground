from string import Template
from Config import *

method = "GetProducts"
data = "UHOM180"

messagetemplate = Template(r"""<?xml version="1.0" encoding="utf-8"?>
   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soapenv:Body>
      <$method xmlns="http://www.deschacht.eu/">
         <Login>$login</Login>
         <Password>$password</Password>
         <ProductCodes>$data</ProductCodes>
      </$method>
   </soapenv:Body>
</soapenv:Envelope>""")


body = messagetemplate.substitute(login = login, password = password, data = data, method = method)

result = fire_post_request(url1, body, 60, method)
print(result)

