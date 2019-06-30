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

def get_tid(time=None):
    time = timezone.now().timestamp() if time is None else time
    return math.floor(time / 3600)    # now divide by hour, able to change

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_ts():
    # return math.floor(timezone.now().timestamp() / 3600)    # now divide by hour, able to change
    return math.floor(datetime.datetime.now().timestamp())

'''
    Generate timeslot from timestamp.
'''
def generate_timeslot(time=None):
    time = timezone.now().timestamp() if time is None else time
    tid = math.floor(time / 3600)
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) AS cnt FROM maker_relatednews')
        res = dictfetchall(cursor)
        num = res[0]['cnt']
        nid = random.randint(1, num)
        cursor.execute("INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)", [tid, time, nid])
    return tid

'''
    Load the data from the API to a dictionary and also a 
    local cache file. Load every time slot.
'''
def load_data(time=None):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    url2 = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
    parameters = {
        'start': '1',
        'limit': '200',
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
        
        sym_list = ''
        for i in range(len(data['data'])):
            symbol = data['data'][i]['symbol']
            sym_list += symbol
            if i != len(data['data']) - 1: sym_list += ','
        
        params = {'symbol': sym_list}
        response2 = session.get(url2, params=params)
        data2 = json.loads(response2.text)
        for i in range(len(data['data'])):
            symbol = data['data'][i]['symbol']
            data['data'][i]['description'] = data2['data'][symbol]['description']
        
        # write into the cache file
        if time is None:
            cache = open('cache.txt', 'w')
        else:
            cache = open('cache_%s.txt' % time, 'w')
        resp = json.dumps(data, indent=4)
        cache.write(resp)
        cache.close()

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

# only load history to cache but not the database   (200 is currently hardcoded)
def load_history_to_cache(id, sym):
    # get history of symbol from crypto compare API
    if sym == 'MIOTA': symb = 'IOTA'
    else: symb = sym
    api_key = '9e60336ab74b49376ab8d19a2897ad5a23b9235edb1751ebd60cfdec3769f203'
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym=%s&tsym=USD&limit=200&api_key=%s' % (symb, api_key)
    
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
    except KeyboardInterrupt:
        raise
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0

    path = os.path.join('..', 'History', 'history_%s.txt' % sym)
    cache = open(path, 'w')
    cache.write(response.text)
    cache.close()
    return data['Data']
    

'''
    Update historical data and write to Cache for given coin. 
    From crypto compare here. --Song
'''
def load_history_from_cache(id, sym, supply):
    # read data from cache
    path = os.path.join('..', 'History', 'history_%s.txt' % sym)
    cache = open(path, 'r')
    data = json.loads(cache.read())

    # update them into sqlite database: (attribute in doubt: privacy?)
    data = data['Data']
    for r in data:
        tid = generate_timeslot(r['time'])
        mid = (tid % 1e6) * (id % 1e6)
        volume_24h = r['volumeto']      # volume in USD
        if volume_24h == 0: continue
        price = r['open']
        privacy = 8.0
        # utility = value_maker(volume_24h, supply, privacy, price)

        with connection.cursor() as cursor:
            cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, utility, crypto_currency_id, timeslot_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume_24h, privacy, price, supply, 0.1, id, tid] )
    cache.close()

'''
    Insert the history data of all currencies using load_history.
'''
def insert_all_history(sym='BTC'):
    d1 = get_data_from_cache()
    start = False
    for r in d1:
        if r['symbol'] == sym: start = True
        if not start: continue
        try:
            load_history_from_cache(r['id'], r['symbol'], r['circulating_supply'])
            print(' - coin', r['id'], ':', r['symbol'], 'inserted')
        except KeyboardInterrupt:
            raise
        except: 
            print(' - coin', r['id'], ':', r['symbol'], 'ignored')
    complete_time()

'''
    Check and update all the times and newsId in timeslot table.
    Ensure the data integrity in timeslot.
'''
def complete_time():
    with connection.cursor() as cursor:
        cursor.execute(''' SELECT timeslot_id AS id FROM maker_metric
            INTERSECT SELECT id FROM maker_timeslot''')
        res1 = dictfetchall(cursor)
        cursor.execute('SELECT COUNT(*) AS cnt FROM maker_relatednews')
        res2 = dictfetchall(cursor)
    
    if len(res1) == 0: return
    num = res2[0]['cnt']
    print('Incomplete timeslot: ', res1)
    print('# News: ', num)

    for i in range(len(res1)):
        tid = res1[i]['id']
        time = tid * 3600
        nid = random.randint(1, num)
        with connection.cursor() as cursor:
            cursor.execute('INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)', [tid, time, nid])

def update_utility(id, sym, price):
    path = os.path.join('Predict', 'pred_%s.txt' % sym)
    try:
        f = open(path, 'r')
    except:
        print('Cannot open ', path)
        return    
    data = json.loads(f.read())
    f.close()
    utility = round(data['utility'] / price * 100.0, 5)
    data['utility'] = utility
    with connection.cursor() as cursor:
        cursor.execute("UPDATE maker_metric SET utility = %s WHERE crypto_currency_id = %s AND timeslot_id = \
            (SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = %s)", [utility, id, id])
    return data

def update_news(tag, ttype, picture, content, author):
    update_news.i += 1
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_relatednews (id, tag, ttype, picture, content, author) \
            VALUES(%s, %s, %s, %s, %s, %s)", [update_news.i, tag, ttype, picture, content, author])
    
update_news.i = 0       # temp use

#Begin---Zou
def load_news1():
    url = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd7b9c12f8285934f9137a8448308ea51bdc40e47e8608146946b3d471e8f8320',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['Data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return 0

def update_news1():
    data = load_news1()
    print('News about ', data[0]['tags'], ' loaded ')
    for r in data:
        tag = r['tags']
        ttype = r['categories']
        picture = r['imageurl']
        content = r['body']
        author = r['source']
        update_news(tag,ttype,picture,content,author)

