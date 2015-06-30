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
         'color': 'disc',
         'productid': 'disc',
         'price': 'flt'}

mapping = {'header': {'5': 0, '15': 1, '35': 2},
           'adtype': {'skyscraper': 0, 'square': 1, 'banner': 2},
           'color': {'green': 0, 'blue': 1, 'red': 2, 'black': 3, 'white': 4},
           }

mapHeader = {
    '5': 0,
    '15': 0.5,
    '35': 1
}

class Beta():
    def __init__(self):
        self.alpha = 1
        self.beta = 1

    def get(self):
        return scipy.stats.beta(self.alpha, self.beta).rvs()

    def getBest(self):
        return scipy.stats.beta(self.alpha, self.beta).mean()

    def updateAlpha(self, value):
        self.alpha += value

    def updateBeta(self, value):
        self.beta += value

    def add(self, other):
        self.alpha += other.alpha
        self.beta += other.beta


class Betas():
    """ Class that covers multiple betas to use for discrete,
		 non-ordinal variables"""

    def __init__(self, n):
        self.betas = [Beta() for i in range(n)]

    def get(self):
        return [beta.get() for beta in self.betas]

    def getBest(self):
        return [beta.getBest() for beta in self.betas]

    def add(self, other):
        for beta, obeta in zip(self.betas, other.betas):
            beta.add(obeta)

    #TODO: wat is hier fout aan?
    def updateBeta(self, index):
        self.betas.index(index).updateBeta(1)

    def updateAlpha(self, index):
        self.betas.index(index).updateAlpha(1)

class Distribution():
    """ Class that covers all distributions. Call get to get a random value.
		Call fit to update the distribution.
	"""

    def __init__(self, dtype, shape, n=None, mx=None):
        self.dtype = dtype
        if dtype == 'ord':
            self.distribution = Beta()
            self.thresh = 1. / n
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
            return np.int(v / self.thresh)
        elif self.dtype == 'disc':
            vs = self.distribution.get()
            return np.argmax(vs)
        else:
            v = self.distribution.get()
            return self.mn + v * (self.mx - self.mn)

    def getBest(self):
        if self.dtype == 'ord':
            v = self.distribution.getBest()
            return np.int(v / self.thresh)
        elif self.dtype == 'disc':
            vs = self.distribution.getBest()
            return np.argmax(vs)
        else:
            v = self.distribution.getBest()
            return self.mn + v * (self.mx - self.mn)

    def add(self, other):
        self.distribution.add(other.distribution)

    def updateDistribution(self, value, success, key):
        if self.dtype == 'ord':
            if success:
                self.distribution.updateAlpha(mapHeader[value])
            else:
                self.distribution.updateBeta(mapHeader[value])
        elif self.dtype == 'disc':
            #TODO: wat is hier fout aan?
            if success:
                print mapping[key][value]
                self.distribution.updateAlpha(mapping[key][value])
            else:
                print mapping[key][value]
                self.distribution.updateBeta(mapping[key][value])
        else:
            if success:
                self.distribution.updateAlpha(float(value)/50)
            else:
                self.distribution.updateBeta(1 - (float(value)/50))

class DataGenerator():
    def __init__(self, models=None):
        if models is None:
            self.distribution = {
                'header': Distribution(types['header'], 'uniform', 3),
                'adtype': Distribution(types['adtype'], 'uniform', 3),
                'color': Distribution(types['color'], 'uniform', 5),
                'productid': Distribution(types['productid'], 'uniform', 16),
                'price': Distribution(types['price'], 'uniform', 0, 50)
            }
        else:
            self.merge(models)

    def getPoint(self, context):
        point = {}
        for key in self.distribution:
            point.update({key: self.distribution[key].get()})
        return point

    def getBestPoint(self, context):
        point = {}
        for key in self.distribution:
            point.update({key: self.distribution[key].getBest()})
        return point

    def updateDistribution(self, ad_data, success):
        for key in self.distribution:
            self.distribution[key].updateDistribution(ad_data[key], success, key)

    def merge(self, models):
        self.distribution = models[0].distribution
        for var in ['header', 'adtype', 'color', 'productid', 'price']:
            for other in models[1:]:
                self.distribution[var].add(other.distribution[var])
