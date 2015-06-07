# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 14:02:12 2015

    Contains a mapping from categories to integers for all
    categorical variables and back again.
    Used to provide a consistent encoding within the entire program.
    (Many classifiers need integers instead of strings or other representations
    of categories within a variable)

@author: Hans-Christiaan
"""
# Note: is in alphabetical order
cat_int_map = {
    'Agent':    {'Linux':0, 'Mobile':1, 'OSX':2, 'Windows':3},
    'Language': {'GE':0, 'EN':1, 'NA':2, 'NL':3},
    'Referer':  {'Bing':0, 'Google':1, 'NA':2},
    'Header':   {'5':0, '15':1, '35':2},
    'Adtype':   {'Banner':0, 'Skyscraper':1, 'Square':2},
    'Color':    {'Black':0, 'Blue':1, 'Green':2, 'Red':3, 'White':4} 
}

int_cat_map = {
    'Agent':    {0:'Linux', 1:'Mobile', 2:'OSX', 3:'Windows'},
    'Language': {0: 'GE', 1: 'EN', 2: 'NA', 3: 'NL'},
    'Referer':  {0: 'Bing', 1: 'Google', 2: 'NA'},
    'Header':   {0: '5', 1: '15', 2: '35'},
    'Adtype':   {0: 'Banner', 1: 'Skyscraper', 2: 'Square'},
    'Color':    {0: 'Black', 1: 'Blue', 2: 'Green', 3: 'Red', 4: 'White'}
}

# Calculate the number of categories in each variable in cat_int_map
n_cat = {var: len(cats) for (var, cats) in cat_int_map.iteritems()}

def factorize_new(data):
    fact = []
    for item in data:
        if type(item) is str:
            for var in cat_int_map:
                if item in cat_int_map[var]:
                    fact = fact + cat_int_map[var][data[var]]
    return fact

def factorize(data):
    fact = []
    for var in data:
        fact = fact + cat_int_map[var][data[var]]
    return fact    

# code for generating int_cat_map from cat_int_map (or vice-versa)
#for var in cat_int_map.iterkeys():
#    int_cat_map[var] = dict(reversed(item) for item in cat_int_map[var].items())



