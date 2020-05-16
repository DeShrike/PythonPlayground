import time
import requests

# STAGING: https://sta-schac-ecommerce.natchcloud.com/
# LIVE: https://shop.deschacht.eu/

hostname = 'sta-schac-ecommerce.natchcloud.com'
# hostname = 'shop.deschacht.eu'

url1 = 'https://' + hostname + '/ws/eservices.asmx'		
url2 = 'https://' + hostname + '/ws/ecatalog.asmx'		
login = "user@company.be"		# <-- your username here
password = "secret"			# <-- your password here
hsh = "4398-1c2bdd3d3ee4fc5e7dee1b86093dd929"		# get this from the CreateUserhash method

headers = {
  'Content-Type': 'text/xml;charset=UTF-8', 
  'Host': hostname, 			
  'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)',
  'Pragma': 'no-cache'
  }

def fire_post_request(url, data, timeout, method):
	headers["SOAPAction"] = '"http://www.deschacht.eu/' + method + '"'
	start_time = time.time()
	response = requests.post(url, data = data, timeout = timeout, headers = headers)
	end_time = time.time() - start_time
	return {'responsetime': end_time, 'response': response.text}
