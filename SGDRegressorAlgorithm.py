# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 12:18:06 2015

@author: Hans-Christiaan
"""

from sklearn.linear_model import SGDRegressor
import pickle
import random as rnd
import algorithm
import categoryMapping as cm

class SGDRegressorAlgorithm(algorithm.Algorithm):

    def __init__(self):
        self.regressor = SGDRegressor()
        
    
    def make_selection(self, context):
        """ Expects a context of
			user_id, agent, language, age, referer
			Produces a set of
			header, ad_type, color, product_id, price
			To learn from
		"""
        header = rnd.choice(['5','15','35'])
        ad_type = rnd.choice(['Banner','Skyscraper','Square'])
        color = rnd.choice(['Black','Blue','Green','Red','White'])
        product_id = rnd.randint(10,26)
        price = rnd.randint(0,50)
        
        return header, ad_type, color, product_id, price
        
        #return {'Header': header, 'Adtype': ad_type, 'Color': color,
        #            'ProductID': product_id, 'Price': price}


    def learn(self, context, ad_data, result):
        """ Expects a context of
			user_id, agent, language, age, referer
			ad_data:
			header, ad_type, color, product_id, price
			result:
			boolean or {success/failure}
			To learn from
		"""
        context = cm.factorize(context)
        ad_data = cm.factorize(ad_data)
        x = context + ad_data
        y = result
        self.regressor = self.regressor.partial_fit([x],[y])
		

    def save(self):
        """ Saves the model, overwrites previous models """
        pickle.dump(self.regressor, open("saved_models/SGDModel.p","wb"))  


    def predict(self, context):
        """ Like giveselection, but tries to maximize gain 
			as opposed to information
		"""
        max_price = 0
        # brute-force way to get the parameters of the ad that
        # gives the best price
        for header in range(0,cm.n_cat['Header']-1):
            for ad_type in range(0,cm.n_cat['Adtype']-1):
                for color in range(0,cm.n_cat['Color']-1):
                    for product_id in range(10,26):
                        for price in range(0,50):
                            x = context + (header, ad_type, color, product_id, price)
                            pred = self.regressor.predict(x)
                            if pred is 1:
                                max_price = max(price, max_price)
                        
