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
			res=res+self.get_all_transactions(address,res[9999]['blockNumber'],end)
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
				if transactions[i]["from"] not in investors:
					investors[transactions[i]["from"]]=self.convert_dollar(transactions[i]["value"], self.rate)
				else:
					investors[transactions[i]["from"]]=investors[transactions[i]["from"]]+self.convert_dollar(transactions[i]["value"], self.rate)
		return investors

	def investors_to_csv(self, address, file_address):
		investors=self.get_investors_dollars(address)
		investments=[]
		for i in investors:
			investments.append([i,investments[i]])
		pd.DataFrame(investments, columns=["From", "Value"]).to_csv(file_address)

	def get_balance(self, address):
		apirequest="https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey="+self.apikey
		r = requests.get(url=apirequest)
		return float(r.json()["result"])

	def get_balance_dollar(self, address):
		apirequest="https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey="+self.apikey
		r = requests.get(url=apirequest)
		return convert_dollar(r.json()["result"])

	def get_all_useful_transactions(self, address):
		transactions=self.get_all_transactions(address)
		useful_transactions=[]
		for trs in transactions:
			useful_transactions.append([trs["from"],trs["to"], trs["value"], trs["blockNumber"]])
		return useful_transactions

	def transactions_to_csv(self, address, file_address):
		transactions=pd.DataFrame(self.get_all_useful_transactions(address), columns=["From", "To", "Value", "Block"])
		transactions.to_csv(file_address)

	def get_transaction_values(self, address):
		transactions=self.get_all_useful_transactions(address)
		transactions_values={}
		for trs in transactions:
			if (trs[0],trs[1]) in transactions_values:
				transactions_values[(trs[0],trs[1])]=transactions_values[(trs[0],trs[1])]+trs[2]
			else:
				transactions_values[(trs[0],trs[1])]=trs[2]
		return transactions_values


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