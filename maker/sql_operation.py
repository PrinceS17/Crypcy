from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from maker.models import *

import datetime
import json
import sqlite3
import math
import random
#import pymysql

def get_tid():
    return math.floor(timezone.now().timestamp() / 3600)    # now divide by hour, able to change

def make_tid():
    return math.floor(get_tid() - 5 + random.randint(0, 10) )

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update_news(tag, ttype, picture, content, author):
    update_news.i += 1
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_relatednews (id, tag, ttype, picture, content, author) \
            VALUES(%s, %s, %s, %s, %s, %s)", [update_news.i, tag, ttype, picture, content, author])

update_news.i = 0       # temp use

'''
    Schedule time and load data every time slot.
'''
def update_timeslot():
    tid = get_tid()
    if tid == update_timeslot.id:   # avoid duplicate id
        return
    update_timeslot.id = tid
    time = timezone.now().timestamp()       # field type is TimeField, should be ok
    if update_news.i == 0:
        update_news('holder', 'test', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Exam is coming!', 'Jason')
        nid = 1
    else:
        nid = random.randint(1, update_news.i)
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)", [tid, time, nid])

update_timeslot.id = 0      # temp use


'''
    Make up time in [now - 5, now + 5].
'''
def makeup_timeslot():
    tid = make_tid()
    makeup_timeslot.id = tid
    time = timezone.now().timestamp() - 10
    if update_news.i == 0:
        update_news('holder', 'test', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Exam is coming!', 'Jason')
        nid = 1
    else:
        nid = random.randint(1, update_news.i)
    with connection.cursor() as cursor:
        cursor.execute("INSERT OR REPLACE INTO maker_timeslot (id, time, related_news_id) \
            VALUES(%s, %s, %s)", [tid, time, nid])

makeup_timeslot.id = 0


'''
def update_user():

def update_favorite():

def update_log():

'''

'''
    Delete a certain kind of currency, e.g. delete_currency(name='Bitcoin').
    Return True if success.
'''
def delete_currency(**kwargs):
    for k in kwargs:
        try:
            if k == 'name':
                q = CryptoCurrency.objects.get(name=kwargs[k])
            elif k == 'id':
                q = CryptoCurrency.objects.get(id=kwargs[k])
        except ObjectDoesNotExist:
            print("Object doesn't exist! ")
            return False
        q.delete()
        return True


'''
    Load the data from the API to a dictionary and also a
    local cache file. Load every time slot.
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
    Get crypto currency data from cache but not website API.
    Return the data part of cache, i.e. a list of all entry dictionaries.
'''
def get_data_from_cache():
    cache = open('cache.txt', 'r')
    data_all = json.loads(cache.read())
    cache.close()
    return data_all['data']


'''
    Insert/update the specified record related to crypto currency.
    Maybe from online or local cache file.
    Input the search keyword like name='bitcoin' or logo='xxx'.
'''
def update_currency(mode, **kwargs):
    data = get_data_from_cache()
    if mode == 'get':
        tid = get_tid()             # note tid should already exist in table! or foreign key constraint will fail
    elif mode == 'make':
        if makeup_timeslot.id > 0:
            tid = makeup_timeslot.id
        else:
            tid = make_tid()

    # insert/update the record by keyword, 1 by default
    for r in data:
        for k in kwargs:
            if r[k] == kwargs[k]:
                mid = (tid % 1e6) * (r['id'] % 1e6)
                supply = r['circulating_supply']
                price = r['quote']['USD']['price']
                volume = r['quote']['USD']['volume_24h']
                privacy = 9.0        # in doubt, where privacy in [0, 10]
                utility = (volume / supply) * math.log10(privacy + 1) / price   # formula by intuition

                logo = 'https://s2.coinmarketcap.com/static/img/coins/32x32/%s.png' % r['id']

                # connect to database
                with connection.cursor() as cursor:
                    cursor.execute("INSERT OR REPLACE INTO maker_cryptocurrency (id,name,logo) \
                        VALUES(%s,%s,%s)", [r['id'], r['name'], logo] )

                    # here need time slot to determine the metric id
                    cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, utility, crypto_currency_id, timeslot_id) \
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume, privacy, price, supply, utility, r['id'], tid] )

# serach by prefix
def search_by_prefix(pref):
    #connet to database
    curren_obj=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE name LIKE %s%%'% [pref]);
    retlist=[];
    for i in curren_obj:
        curtuple=(i.id,i.name,i.logo);
        retlist.append(curtuple);
    return retlist;  #organize all outputs into a tuple list

# sort by price, ascending
def sort_by_price():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY price');
    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;

#sort by volume, descending
def sort_by_volume():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY volume DESC');
    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;

#sort by supply, descending
def sort_by_supply():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY supply DESC');

    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;

#sort by utility, descending
def sort_by_utility():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY utility DESC');

    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attributes into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;
