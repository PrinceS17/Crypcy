from rest_framework import generics
from django.http import HttpResponse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3

from . import models
from . import serializers

# dependent of advance function 1
import numpy
import collections
import operator

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

'''
    Advance function 1: 
    Based the total number of coin that user wants and his interested investment 
    risk type (low, moderate, high), give our advice on the combination of currencies.
    Advance because it involves the history data analysis and customed combination
    of currencies based on user's choice.      -- Song
'''
def currency_advice(request, num, type):
    # fetch (currency_id, price) for variance calculation
    with connection.cursor() as cursor:
        cursor.execute('''SELECT crypto_currency_id AS id, price FROM maker_metric''')
    tmp = dictfetchall(cursor)
    prices = {}                 # dict: {id:[price 1, price 2, ...]}
    variance = {}               # dict: {id: variance}
    for e in tmp:
        if e['id'] not in prices:
            prices[e['id']] = [ e['price'] ]
        else: prices[e['id']] += [ e['price'] ]
    
    for id in prices:
        variance[id] = numpy.var(prices[id])
    variance = sort_dict(variance, False)          

    # fetch (currency_id, cur_utility) for utility evaluation (use latest data)
    with connection.cursor() as cursor:
        cursor.execute('''SELECT crypto_currency_id AS id, utility FROM maker_metric m
                        WHERE timeslot_id = (
                            SELECT MAX(timeslot_id) FROM maker_metric m1
                            WHERE m1.crypto_currency_id = m.crypto_currency_id
                        )''')
    tmp_uti = dictfetchall(cursor)
    cur_utility = {}
    for e in tmp_uti:
        cur_utility[e['id']] = e['utility']

    # classify the currency into 3 groups based on variance (high, moderate, low)
    grps = {}                   # dict of dict
    i = 0
    for id in variance:
        tag = i * 3 / len(variance)
        if tag not in grps:
            grps[tag] = {id:cur_utility[id]}
        else: grps[tag][id] = cur_utility[id]
        i += 1

    for tag in grps:
        grps[tag] = sort_dict(grps[tag], True)  # sort the 3 groups by utility
        print(grps[tag])                        # debug here

    # fetch id, name, logo, current price & utility & return list of dict (based on given num and risk type)
    queries = []
    res = []
    if type == 'low':
        ttag = 0
    elif type == 'moderate':
        ttag = 1
    else: ttag = 2
    i = 0
    for id in grps[ttag]:       # for loop: easy to extend to N currencies
        queries += ['''SELECT cid, name, logo, price, utility
                    FROM ( SELECT id AS cid, name, logo FROM maker_cryptocurrency c WHERE id = %s ) 
                        JOIN maker_metric m ON cid = m.crypto_currency_id
                    WHERE m.timeslot_id = (
                        SELECT MAX(timeslot_id) FROM maker_metric m1
                        WHERE m1.crypto_currency_id = cid
                    ) ''' % (id)]
        with connection.cursor() as cursor:
            cursor.execute(queries[i])
        res += dictfetchall(cursor)
        i += 1
        if i > 3: break

            
    res_json = json.dumps(res)
    return HttpResponse(res_json)

def sort_dict(d, is_reverse):
    sorted_x = sorted(d.items(), key=operator.itemgetter(1), reverse=is_reverse)    # sorted by var value
    return collections.OrderedDict(sorted_x)                                        # return the dict