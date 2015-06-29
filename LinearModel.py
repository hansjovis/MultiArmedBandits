from AssumptionAnnealing import Model
from numpy.random import uniform
from sklearn.linear_model import LinearRegression as LR
import categoryMapping as cm

class LinearModel(Model):
	""" Linear extendable model
	"""
	
	def __init__(self):
		super(self)
		self.algorithm = LR()
	
	def choose(self, context, epsilon):
		if uniform < epsilon:  # Explore
			header = rnd.choice(['5','15','35'])
			ad_type = rnd.choice(['Banner','Skyscraper','Square'])
			color = rnd.choice(['Black','Blue','Green','Red','White'])
			product_id = rnd.randint(10,26)
			price = rnd.randint(0,50)
			return header, ad_type, color, product_id, price
		else:  # Exploit
			max_price = 0
			max_v = []
			# brute-force way to get the parameters of the ad that
			# gives the best price
			for header in range(0,cm.n_cat['Header']-1):
				for ad_type in range(0,cm.n_cat['Adtype']-1):
					for color in range(0,cm.n_cat['Color']-1):
						for product_id in range(10,26):
							for price in range(0,50):
								x = context + (header, ad_type, color, product_id, price)
								pred = self.algorithm.predict(x)
								if pred is 1:
									if price > max_price:
										max_price = price
										max_v = [header, ad_type, color, product_id, price]
			
			return max_v
		
	def learn(self, context, choices, result):
		context = cm.factorize(context)
		choices = cm.factorize(choices)
		self.algorithm = self.algorithm.partial_fit([context + choices], [result])
	
	def extend(self, var):
		`
