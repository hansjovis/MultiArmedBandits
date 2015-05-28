# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:35:49 2015

@author: Hans-Christiaan
"""

import json

TEAM_ID = "TheMulti-ArmedBandits"
TEAM_PW = "???"

CONTEXT_JSON_TEST = "{ \"context\": { \"Age\": 25.0, \"Agent\": \"mobile\",\
 \"ID\": 339, \"Language\": \"GE\", \"Referer\": \"Bing\" } }"
EFFECT_JSON_TEST = "{ \"effect\": { \"Error\": null, \"Success\": 0 } }"

def getContext(run_id, i):
    """ Gets a simulated interaction from a user with the webpage
        from the server.
    """
    
    
    
    
    
    context_obj = json.loads(CONTEXT_JSON_TEST)['context']
    
    user_id     = context_obj['ID']
    agent       = context_obj['Agent']
    language    = context_obj['Language']
    referer     = context_obj['Referer']
    age         = context_obj['Age']
    
    return user_id, agent, language, age, referer  

def proposePage(run_id, i, header, ad_type, color, product_id, price):
    """ Proposes the parameters of the ad to show to the interaction i
        from run number run_id. Returns whether the user buys the product
        or not.
    """
    
    
    
    effect_obj = json.loads(EFFECT_JSON_TEST)['effect']
    
    error   = effect_obj['Error']
    if error is not 'null':
        raise RuntimeError('proposePage: passed the wrong arguments.')
        
    success = effect_obj['Success']
    return success


    