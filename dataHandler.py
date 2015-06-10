""" This class generates data points for every free variable.
    The data points are generated from a distribution.
    TODO: This distribution can then be updated based on the result.
	TODO: Distributions and learning based on context
	Usage:
	>> dg = dataHandler.dataGenerator()
	>> dg.getPoint(CONTEXT)
"""
import scipy.stats
import numpy as np


types = {'header': 'ord',
		 'adtype': 'disc',
		 'color':  'disc',
		 'productid': 'disc',
		 'price': 'flt'}

class Beta():
	def __init__(self):
		self.alpha = 1
		self.beta  = 1
	
	def get(self):
		return scipy.stats.beta(self.alpha, self.beta).rvs()
	
class Betas():
	""" Class that covers multiple betas to use for discrete,
		 non-ordinal variables"""
	def __init__(self, n):
		self.betas = [Beta() for i in range(n)]
	
	def get(self):
		return [beta.get() for beta in self.betas]

class Distribution():
	""" Class that covers all distributions. Call get to get a random value.
		Call fit to update the distribution.
	"""
	def __init__(self, dtype, shape, n=None, mx=None):
		self.dtype = dtype
		if dtype == 'ord':
			self.distribution = Beta()
			self.thresh = 1./n
		elif dtype == 'disc':
			self.n = n
			self.distribution = Betas(n)
		elif dtype == 'flt':
			self.distribution = Beta()
			self.mn = n
			self.mx = mx
	
	def get(self):
		if self.dtype == 'ord':
			v = self.distribution.get()
			return np.int(v/self.thresh)
		elif self.dtype == 'disc':
			vs = self.distribution.get()
			return np.argmax(vs)
		else:
			v = self.distribution.get()
			return self.mn + v * (self.mx - self.mn)

class DataGenerator():
	def __init__(self):
		self.distribution = {
			'header': Distribution(types['header'], 'uniform', 3),
			'adtype': Distribution(types['adtype'], 'uniform', 3),
			'color':  Distribution(types['color'],  'uniform', 5),
			'productid': Distribution(types['productid'], 'uniform', 16),
			'price': Distribution(types['price'], 'uniform', 0, 50)
		}
	
	def getPoint(self, context):
		point = {}
		for key in self.distribution:
			point.update({key: self.distribution[key].get()})
		return point
