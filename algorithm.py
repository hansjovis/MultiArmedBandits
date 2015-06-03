import pickle

class Algorithm:
	def make_selection(self, context):
		""" Expects a context of
			user_id, agent, language, age, referer
			Produces a set of
			header, ad_type, color, product_id, price
			To learn from
		"""
		pass
	
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
		pass

	def predict(self, context):
		""" Like giveselection, but tries to maximize gain 
			as opposed to information
		"""
		pass
