__author__ = 'Senna'

import requests

def get(url, params):
    # make a get request
    while True:
        try:
            return requests.get(url, params = params)
        except requests.ConnectionError:
            pass

def post(url, params):
    # make a post request
    while True:
        try:
            return requests.post(url, params = params)
        except requests.ConnectionError:
            pass

def getContent(r):
    return r.text

def getJSON(r):
    return r.json()
