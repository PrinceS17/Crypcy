from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import datetime
import json
import sqlite3
import math
import random
import os

# rewrite 
def get_tid():
    # return math.floor(timezone.now().timestamp() / 3600)    # now divide by hour, able to change
    return math.floor(datetime.datetime.now().timestamp() / 3600)

def get_ts():
    # return math.floor(timezone.now().timestamp() / 3600)    # now divide by hour, able to change
    return math.floor(datetime.datetime.now().timestamp())


'''
    Load the data from the API to a dictionary and also a 
    local cache file. Load every time slot.
'''
def load_data(time=None):
    if time is None: time = ''
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '120',
        'convert': 'USD',
        #'sort': 'price',
        #'sort_dir':'desc',
        #'cryptocurrency_type':'coins'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'fc5c03fd-2394-4df2-8e25-20dd037536a0',
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # write into the cache file
        try:
            os.mkdir('Cache')
        except OSError:
            # print('Cache exists!')
            pass
        else: pass
        fname = os.path.join('Cache', 'cache_%s.txt' % time)
        cache = open(fname, 'w')
        cache.write(response.text)
        cache.close()
        print('%s loaded...' % fname)
        return data['data']
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0

'''
    Get crypto currency data from cache but not website API.
    Return the data part of cache, i.e. a list of all entry dictionaries.
'''
def get_data_from_cache(time=None):
    if time is None:
        cache = open(os.path.join('..', 'cache.txt'), 'r')
    else:
        cache = open(os.path.join('..', 'cache_%s.txt' % time), 'r')
    data_all = json.loads(cache.read())
    cache.close()
    return data_all['data']
