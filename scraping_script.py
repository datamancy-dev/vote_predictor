import requests
import pandas as pd
import pickle
import requests

script, keyfile = argv
key = ''
with open(keyfile, 'r') as f:
    for line in f:
        key = line

PAYLOAD = {'X_API_Key':key}


