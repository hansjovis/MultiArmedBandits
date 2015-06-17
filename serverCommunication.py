# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:35:49 2015

@author: Hans-Christiaan
"""

from config import config
import handleRequests as hr

TEAM_ID = "TheMulti-ArmedBandits"
TEAM_PW = "???"

EFFECT_JSON_TEST = "{ \"effect\": { \"Error\": null, \"Success\": 0 } }"

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
    
    return user_id, agent, language, age, referer  


def proposePage(run_id, i, header, adtype, color, productid, price):
    """ Proposes the parameters of the ad to show to the interaction i
        from run number run_id. Returns whether the user buys the product
        or not.
    """
    
    params = {  'teamid':config['teamid'],
                'teampw':config['teampw'],
                'runid':run_id,
                'i':i,
                'header':header,
                'adtype':adtype,
                'color':color,
                'productid':productid,
                'price':price }
    # make a request to the server
    req = hr.get(config['proposeurl'], params)
	
    if 'error' in hr.getJSON(req):
        raise RuntimeError('proposedPage: something else went wrong with:\n{}\n{}'.format(hr.getJSON(req), params))
    
    # get the server's response in JSON-form    
    effect = hr.getJSON(req)['effect'] 

    error   = effect['Error']
    if error is not None:
        raise RuntimeError('proposePage: passed the wrong arguments.\n{}\n{}'.format(hr.getJSON(req), params))
        
    success = effect['Success']
    return success


    
