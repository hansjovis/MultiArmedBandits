import pickle
import os
import dataHandler

mapping = {'header': {0: '5', 1: '15', 2: '35'},
		   'adtype': {0: 'skyscraper', 1: 'square', 2: 'banner'},
		   'color':  {0: 'green', 1: 'blue', 2: 'red', 3: 'black', 4: 'white'},
		  }

class Algorithm:
	def __init__(self, model=None):
		""" Constructor for Algorithm.
			Optional arg model: if string, loads corresponding file
								unless it is 'latest', then loads latest
								if DataGenerator, uses that as model
								else (if None) creates new model
		"""
		if model is None:
			self.predictor = dataHandler.DataGenerator()
		elif type(model) == str:
			if model == 'latest':
				i = 0
				while os.path.exists("models/model{}".format(i)):
					i+=1
				self.predictor = pickle.load("models/model{}".format(i-1))
			else:
				self.predictor = pickle.load("models/" + model)
		else:
			self.predictor = model
	
	def convert(self, data):
		""" Uses mapping as defined above to map integers to their
			discrete representations.
		"""
		if 'productid' in data:
			data['productid'] = data['productid'] + 10
		if 'price' in data:
			from decimal import Decimal
			data['price'] = Decimal(data['price']).quantize(Decimal('0.01')).to_eng_string()
		for key in data:
			if key in mapping:
				data[key] = mapping[key][data[key]]
		return data
	
	def make_selection(self, context):
		""" Expects a context of
			user_id, agent, language, age, referer
			Produces a set of
			header, ad_type, color, product_id, price
			To learn from
		"""
		return self.convert(self.predictor.getPoint(context))
	
	def learn(self, context, ad_data, result):
		""" Expects a context of
			user_id, agent, language, age, referer
			ad_data:
			header, ad_type, color, product_id, price
			result:
			boolean or {success/failure}
			To learn from
		"""
		pass
	
	def save(self, model=None):
		""" Saves the model to new file """
		if model is None:
			model = self.lastmodel()
		with open("models/model{}".format(model+1), 'wb') as openfile:
			pickle.dump(self.predictor, openfile)
	
	def lastmodel(self):
		i = 0
		while os.path.exists("models/model{}".format(i)):
			i+=1
		return i-1
	
	def load(self, name=None):
		if name is None:
			name = self.lastmodel()
		with open("models/" + name) as openfile:
			return pickle.load(openfile)

	def predict(self, context):
		""" Like giveselection, but tries to maximize gain 
			as opposed to information
		"""
		pass
