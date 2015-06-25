# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:35:12 2015

@author: Hans-Christiaan
"""

import algorithm
import random as rnd
import pandas as pd

DATABASE_PATH = "database.csv"
COLUMNS = ["Agent","Language","Age","Referer","Header","Adtype","Color","Productid","Price"]

class GeneticAlgorithm(algorithm.Algorithm):

    def __init__(self):
        self.database = pd.read_csv(DATABASE_PATH,index_col='ID')


    def make_selection(self, context):
        """ Expects a context of
            user_id, agent, language, age, referer
            Produces a set of
            header, ad_type, color, product_id, price
            To learn from
        """
        return self.randomSelection()

    def randomSelection(self):
        header = rnd.choice(['5','15','35'])
        ad_type = rnd.choice(['Banner','Skyscraper','Square'])
        color = rnd.choice(['Black','Blue','Green','Red','White'])
        product_id = rnd.randint(10,26)
        price = rnd.randint(0,50)

        return header, ad_type, color, product_id, price

    def learn(self, context, ad_data, result):
        """ Expects a context of
            user_id, agent, language, age, referer
            ad_data:
            header, ad_type, color, product_id, price
            result:
            boolean or {success/failure}
            To learn from
        """        
        if result == 1:            
            data = list(context[1:] + ad_data)
            data_dict = {COLUMNS[i]: [data[i]] for i in range(0,len(COLUMNS)) }                        
            new_row = pd.DataFrame(data_dict, index=[context[0]])            
            print "success!"                       
            self.database = self.database.append(new_row)                       


    def save(self):
        """ Saves the model, overwrites previous models """
        self.database.to_csv(DATABASE_PATH)

    def predict(self, context):
        """ Like giveselection, but tries to maximize gain
            as opposed to information
        """
        pass