import requests
import pandas as pd
import os
import sys
import logging

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('%(asctime)s : %(processName)s : %(levelname)s : %(message)s'))
logger.addHandler(log_handler)

class EthScrapping():
	def __init__(self, apikey, rate=200, logging_level="DEBUG"):
		self.apikey=apikey
		self.rate=rate
		logger.setLevel(logging.getLevelName(logging_level))

	#Limit 10.000
	def get_transactions(self,address, start=0, end=99999999):
		apirequest="http://api.etherscan.io/api?module=account&action=txlist&address="+address+"&startblock="+str(start)+"&endblock="+str(end)+"&sort=asc&apikey="+self.apikey
		r = requests.get(url=apirequest)
		return r.json()["result"]

	#All transactions recorded
	def get_all_transactions(self, address, start=0, end=99999999):
		apirequest="http://api.etherscan.io/api?module=account&action=txlist&address="+address+"&startblock="+str(start)+"&endblock="+str(end)+"&sort=asc&apikey="+self.apikey
		r = requests.get(url=apirequest)
		res=r.json()["result"]
		if (len(res)==10000):
			res=res+get_all_transactions(address,res[9999]['blockNumber'],end)
		return res

	def get_investors(self, address):
		transactions=self.get_all_transactions(address, start=0, end=99999999)
		investors={}
		for i in range(len(transactions)):
			if transactions[i]["to"]==address:
				investors[transactions[i]["from"]]=self.convert_dollar(transactions[i]["value"])
		return investors

	def convert_dollar(self, value, rate):
		return float(value)*rate/1000000000000000000

	def get_investors_dollars(self, address):
		transactions=self.get_all_transactions(address, start=0, end=99999999)
		investors={}
		for i in range(len(transactions)):
			if transactions[i]["to"]==address:
				investors[transactions[i]["from"]]=self.convert_dollar(transactions[i]["value"], self.rate)
		return investors

	def get_balance(self, address):
		apirequest="https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey="+self.apikey
		r = requests.get(url=apirequest)
		return float(r.json()["result"])

	def get_balance_dollar(self, address):
		apirequest="https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey="+self.apikey
		r = requests.get(url=apirequest)
		return convert_dollar(r.json()["result"])



if __name__ == '__main__':

	if len(sys.argv) > 1:
		apiKey=sys.argv[1]
		scrapper=EthScrapping(apiKey)
		if len(sys.argv)>2:
			address=sys.argv[2]
		else:
			address="0xd24400ae8BfEBb18cA49Be86258a3C749cf46853"
		print(scrapper.get_transactions(address))
	else:
		print("Error. No API key given.")