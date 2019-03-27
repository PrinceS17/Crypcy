from django.http import HttpResponse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3
#import pymysql

def index(request):
    return HttpResponse("Hello, world. You're at the maker index.")

'''
    Load the data from the API to a dictionary and also a 
    local cache file.
'''
def load_data():
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
        'X-CMC_PRO_API_KEY': '441cb5ae-6618-4110-8db9-df9cba2b05ec',
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # write into the cache file
        cache = open('cache.txt', 'w')
        cache.write(response.text)
        cache.close()

        return data['data']
    
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0


'''
    Insert/update the specified record into database. 
    Maybe from online or local cache file.
'''
def update_record():
    cache = open('cache.txt', 'r')
    data_all = cache.read()
    data = data['data']
    for k in data:
        print(k)

    cache.close()