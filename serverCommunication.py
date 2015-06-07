# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:35:49 2015

@author: Hans-Christiaan
"""

from config import config
import time
import handleRequests as hr

def getContext(run_id, i):
    """ Gets a simulated interaction from a user with the webpage
        from the server.
    """ 

    params = {  'teamid':config['teamid'], 
                'teampw':config['teampw'], 
                'runid':run_id, 
                'i':i }
    # make a request to the server            
    req = hr.get(config['contexturl'], params)
    # get the response in JSON-form
    context = hr.getJSON(req)['context']
    # get the parameters from the JSON-object 'context'    
    user_id     = context['ID']
    agent       = context['Agent']
    language    = context['Language']
    referer     = context['Referer']
    age         = context['Age']
    
    return user_id, str(agent), str(language), age, str(referer)
    #return {'ID':user_id, 'Agent':agent, 'Language':language, 'Age':age, 'Referer':referer}  


def proposePage(run_id, i, header, ad_type, color, product_id, price):
    """ Proposes the parameters of the ad to show to the interaction i
        from run number run_id. Returns whether the user buys the product
        or not.
    """
    
    params = {  'teamid':config['teamid'],
                'teampw':config['teampw'],
                'runid':run_id,
                'i':i,
                'header':header,
                'adtype':ad_type,
                'color':color,
                'productid':product_id,
                'price':price }
    
    # make a request to the server
    req = hr.get(config['proposeurl'], params)
    time.sleep(0.25)
    # get the server's response in JSON-form    
    effect = hr.getJSON(req)['effect'] 
    
    error   = effect['Error']
    if error is not None:
        raise RuntimeError('proposePage: passed the wrong arguments.')
        
    success = effect['Success']
    return success


    