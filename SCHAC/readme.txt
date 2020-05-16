Deschacht Plastics Webservice Python Samples
--------------------------------------------

1. Edit Config.py 
	Replace the login and password placeholders with your login and password.

2. Make sure you have Python 3.x installed
	https://www.python.org/downloads/

3. Install required modules

	In a DOS box, type the following
 
		pip install requests

4. From a DOS box, execute the samples

	To validate your login and password:
		python CheckLogin.py

	To get the contents of your basket:
		python GetBasket.py

	To remove everything from your basket
		python EmptyBasket.py

	To get details of one or more products:
		python GetProducts.py

	To get a user hash (needed for certain methods):
		python CreateUserhash.py

	To search for products:
		python GetProductCodes

	To submit an order:
		python SubmitOrder.py

