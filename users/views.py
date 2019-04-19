from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import permissions, serializers, generics
from rest_framework.generics import RetrieveUpdateAPIView
from . import models
from .serializers import *

from django.http import HttpResponse
from django.db import connection

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3

# dependent of advance function 1
import numpy
import collections
import operator

class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer

class CustomDetailView(RetrieveUpdateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


'''
    Advance function 1: 
    Based the total number of coin that user wants, his interested investment 
    risk type (low, moderate, high) and his favorite coins, give our advice on the 
    combination of currencies.
    Advance because it involves the history data analysis and customed combination
    of currencies based on user's choice and favorites.      -- Song
'''
def currency_advice(request):
    # get parameters from url
    username = request.GET.get('username', '')
    num = int(request.GET.get('num', ''))
    typ = request.GET.get('type', '')
    print('\n\nusername: ', username, ' num: ', num, ' risk type: ', typ, '\n')

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
    variance = sort_dict(variance, False)           # ASC
    print('variance sorted!')
    f1 = open('variance_cache.txt', 'w')
    f1.write(json.dumps(variance, indent=4))
    f1.close()

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
        tag = int(numpy.floor(i * 3 / len(variance)))
        if i < len(variance) * 0.3: tag = 0                 #  < lowTh: low variance
        elif i > len(variance) * 0.85: tag = 2           #  > highTh: high variance
        else: tag = 1

        if id is None: continue
        elif id not in cur_utility: continue
        if tag not in grps:
            grps[tag] = {id:cur_utility[id]}
        else: grps[tag][id] = cur_utility[id]
        i += 1

    if typ == 'low': ttag = 0
    elif typ == 'moderate': ttag = 1
    else: ttag = 2
    
    print('group determined!')

    # here we get utility and variance table in grps[0]/[1]/[2]
    # now time to select favorite and call KNN
    fav_list = get_favorite(username)
    print('favorite id got!')

    chosen_coin = closest_coin(num, fav_list, variance, grps[ttag])

    # fetch id, name, logo, current price & utility & return list of dict (based on given num and risk type)
    res = []
    for id in chosen_coin:       # for loop: easy to extend to N currencies
        query = '''SELECT cid, name, logo, price, utility
                    FROM ( SELECT id AS cid, name, logo FROM maker_cryptocurrency c WHERE id = %s ) 
                        JOIN maker_metric m ON cid = m.crypto_currency_id
                    WHERE m.timeslot_id = (SELECT MAX(timeslot_id) FROM maker_metric m1 WHERE m1.crypto_currency_id = cid
                    ) ''' % id
        with connection.cursor() as cursor:
            cursor.execute(query)
            temp = dictfetchall(cursor)
        temp[0]['variance'] = variance[id]
        res += temp
        if len(res) >= num: break
    res_json = json.dumps(res)
    return HttpResponse(res_json)

def sort_dict(d, is_reverse):
    sorted_x = sorted(d.items(), key=operator.itemgetter(1), reverse=is_reverse)    # sorted by var value
    return collections.OrderedDict(sorted_x)                                        # return the dict

def get_favorite(username):
    # return favorite list of given user
    with connection.cursor() as cursor:
        cursor.execute("SELECT f.cryptocurrency_id AS cid FROM users_customuser u JOIN users_customuser_favorite f \
                    ON u.id = f.customuser_id AND u.username = %s", [username])
        res = dictfetchall(cursor)
    return [r['cid'] for r in res]

def closest_coin(N, target, variance, id_list):
    # return N coins that are closest to target, given a distance function
    # need to get latest metric of each coin: from list view
    # also the min, max, avg, var, volume/supply/utility/variance
    attr = ['volume', 'supply', 'utility']

    # stat = compute_stat(attr, variance)
    stat = load_stat()
   
    print(' -- Computing distance...')
    query = "SELECT * FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id AND me.timeslot_id = \
        (SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = cr.id) AND cr.id = "
    dists_to_target = {}

    for id in id_list:
        if id in target: continue
        with connection.cursor() as cursor:
            cursor.execute(query + str(id))
            r1 = dictfetchall(cursor)
        r1 = r1[0]
        r1['variance'] = variance[id]
        dist_to_target = 0.0
        
        for tgid in target:
            with connection.cursor() as cursor:
                cursor.execute(query + str(tgid))
                r2 = dictfetchall(cursor)
            r2 = r2[0]
            r2['variance'] = variance[tgid]
            
            r1, r2 = standardize(r1, r2, stat)
            dist_to_target += coin_distance(r1, r2)
        dists_to_target[id] = dist_to_target
    
    sort_dists = sort_dict(dists_to_target, False)
    final_list = []
    for k in sort_dists:
        final_list.append(k)
        if len(final_list) == N: break
    return final_list

def compute_stat(attr, variance):
    print(' -- Computing statistics...')
    stat = {}
    for x in attr:
        stat[x] = {}
        with connection.cursor() as cursor:
            cursor.execute('''SELECT sub.a AS av, AVG((m.%s - sub.a) * (m.%s - sub.a)) AS var 
                    FROM maker_metric m, 
                    (SELECT AVG(m1.%s) AS a FROM maker_metric m1 
                        WHERE m1.timeslot_id = (SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = m1.crypto_currency_id)
                    ) AS sub
                    WHERE m.timeslot_id = (SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = m.crypto_currency_id)'''
                    % (x, x, x))
            res = dictfetchall(cursor)
        stat[x]['av'] = res[0]['av']
        stat[x]['var'] = res[0]['var']
    var_list = [variance[id] for id in variance]
    stat['variance'] = {}
    stat['variance']['av'] = numpy.average(var_list)
    stat['variance']['var'] = numpy.var(var_list)

    print(' -- write into cache...')
    f = open('stat_cache.txt', 'w')
    f.write(json.dumps(stat, indent=4))
    f.close()
    return stat

def load_stat():
    print(' -- loading stat ... ')
    f = open('stat_cache.txt', 'r')
    stat = json.loads(f.read())
    return stat

def standardize(r1, r2, stat):
    attr = ['volume', 'supply', 'utility', 'variance']
    for x in attr:
        r1[x] = (r1[x] - stat[x]['av']) / (stat[x]['var'] ** 0.5)
        r2[x] = (r2[x] - stat[x]['av']) / (stat[x]['var'] ** 0.5)
    return r1, r2

def coin_distance(r1, r2):
    # given 2 normalized dictionary of coin, return the distance
    attr = ['volume', 'supply', 'utility', 'variance']
    dist = 0.0
    output = ''
    for x in attr:
        output += str(round((r1[x] - r2[x])**2, 10)) + ', '
        dist += (r1[x] - r2[x])**2
    # print(output)
    return dist ** 0.5
