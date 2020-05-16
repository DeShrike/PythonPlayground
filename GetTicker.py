import requests
import sys
import time
import threading
import os

if len(sys.argv) < 2:
	print("Please supply some coins to track")
	quit()

# eth ltc doge zcl zen etc bch

coin = sys.argv[1]

prices = { 
	"btc": 0.00, 
	"eth": 0.00,
	"ltc": 0.00,
	"doge": 0.00,
	"zcl": 0.00,
	"zen": 0.00,
	"etc": 0.00,
	"bch": 0.00 
}

url = "https://api.bittrex.com/api/v1.1/public/getticker?market=BTC-LTC"

for coin in sys.argv[1:]:
	prices[coin] = 0.00

count = 0

def update_price(coin):
	global count
	while count < 100:
		count = count + 1
		template = "https://api.bittrex.com/api/v1.1/public/getticker?market={}-{}"
		first_coin = "usd" if coin == "btc" else "btc"
		pricing = requests.get(template.format(first_coin, coin)).json()

		prices[coin] = pricing["result"]["Last"]

		time.sleep(3)

for coin, price in prices.items():
	t = threading.Thread(target = update_price, args = (coin,))
	t.start()


while count < 100:
	os.system("cls")
	for coin, price in prices.items():
		usd_price = price * prices["btc"]
		if coin == "btc":
			print("{} -> ${:.2f}".format(coin.ljust(5), price))
		else:
			print("{} -> {:.8f} (${:.2f})".format(coin.ljust(5), price, usd_price))
	time.sleep(0.5)

