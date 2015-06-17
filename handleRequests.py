__author__ = 'Senna'

import requests

def get(url, params):
    # make a get request
    r = requests.get(url, params = params)
    return r

def post(url, params):
    # make a post request
    r = requests.post(url, params = params)
    return r

def getContent(r):
    return r.text

def getJSON(r):
    return r.json()
