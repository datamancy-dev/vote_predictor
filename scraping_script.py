import requests
import pandas as pd
import pickle
import requests

def payload(keyfile):
    """Imports key from file returns GET request payload"""
    key = ''
    with open(keyfile, 'r') as f:
        for line in f:
            key = line

    return {'X_API_Key':key}


