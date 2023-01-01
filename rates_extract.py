import pandas as pd
import numpy as np
import requests
import datetime

class RealTimeCurrencyConverter():
	def __init__(self, url='https://api.exchangerate-api.com/v4/latest/USD'):
		self.url = url
		self.data, self.currencies, self.country_rates = None, None, None
		self.refresh()

	def refresh(self):
		self.data = requests.get(self.url).json()
		self.currencies = self.data['rates']
		self.country_rates = np.array(self.extract_key(self.currencies))
		countries = self.country_rates.T[3]
		indexes = np.argsort(countries)
		self.country_rates = self.country_rates[indexes]

	def extract_key(self, currencies):
		country_key = pd.read_csv("country_code.csv")
		country_key = country_key.values
		country_rates = []
		for key, item in currencies.items():
			try:
				index = np.argwhere(country_key.T[0]==key)[0][0]
				country_rates.append([key, item, country_key.T[1][index], country_key.T[2][index], country_key.T[3][index], country_key.T[4][index], country_key.T[5][index]])
			except:
				pass
		return country_rates

	def convert(self, from_currency, to_currency, amount): 
		initial_amount = amount
		index_from = np.argwhere(self.country_rates.T[0]==from_currency)[0][0]
		index_to = np.argwhere(self.country_rates.T[0]==to_currency)[0][0]
		if from_currency != 'USD' : 
			amount = amount / float(self.country_rates[index_from][1]) 
		amount = round(amount * float(self.country_rates[index_to][1]), 4) 
		return amount

	def save_state(self, path=None):
		if path is None:
			path = "current_conversion_rates_"+str(datetime.datetime.now()).replace(":", "_")
			path = path[:path.index('.')]
			path = path+".csv"
		country_rates = pd.DataFrame(self.country_rates)
		country_rates.columns = ["Key ID", "rate_wrt_USD", "Currency Name", "Country", "Capital", "Lat", "Long"]
		country_rates.to_csv(path, index=False)

if __name__ == '__main__':
	converter = RealTimeCurrencyConverter()
	print(converter.convert('INR','USD',100))
	converter.save_state()