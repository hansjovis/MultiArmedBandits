__author__ = 'Senna'

import requests
from config import config

def get(url, params):
    #print "Tried getting {} on url {}".format(params, url)
    # make a get request
    while True:
        try:
            return requests.get(url, params = params)
        except requests.ConnectionError:
            if config['verbose']:
                print "Connection Error in get"
            pass

def post(url, params):
    # make a post request
    while True:
        try:
            return requests.post(url, params = params)
        except requests.ConnectionError:
            if config['verbose']:
                print "Connection Error in post"
                print "Tried getting {} on url {}".format(params, url)
            pass

def getContent(r):
    return r.text

def getJSON(r):
    return r.json()
