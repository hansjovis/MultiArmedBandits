import pickle
import os
import dataHandler

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
	
	def make_selection(self, context):
		""" Expects a context of
			user_id, agent, language, age, referer
			Produces a set of
			header, ad_type, color, product_id, price
			To learn from
		"""
		return self.predictor.getPoint(context)
	
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
	
	def save(self):
		""" Saves the model, overwrites previous models """
		i = 0
		while os.path.exists("models/model{}".format(i)):
			i+=1
		with open("models/model{}".format(i)) as openfile:
			pickle.dump(self.predictor, openfile)

	def predict(self, context):
		""" Like giveselection, but tries to maximize gain 
			as opposed to information
		"""
		pass
