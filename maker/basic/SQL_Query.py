# Begin Simple SQl Queries
# @author Ruixin Zou
# Latest modified: April 15, Song       1) select *;    2) only display the latest results

import sqlite3
from django.db import connection
from ..sql_operation import *

# search crypto-currencies based on prefix
# prefix: pref
def search_by_prefix(pref):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency as cr, maker_metric as me
        WHERE cr.id=me.crypto_currency_id AND cr.name LIKE "%s%%" AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )''' % pref)
        res=dictfetchall(cursor)
    return res


# sort by price, ascending
def sort_by_price():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id
            AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )
        ORDER BY price''')
        res=dictfetchall(cursor)
    return res

#sort by volume, descending
def sort_by_volume():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id
            AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )
        ORDER BY volume DESC''')
        res=dictfetchall(cursor)
    return res


#sort by supply, descending
def sort_by_supply():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id
            AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )
        ORDER BY supply DESC''')
        res=dictfetchall(cursor)
    return res


#sort by utility, descending
def sort_by_utility():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id
            AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )
        ORDER BY utility DESC''')

        res=dictfetchall(cursor)
    return res

#----end Ruixin Zou

# Start by Song
# filter currencies by price or utility
def filter_coin(p1, p2, u1, u2):
    p1 = 0 if p1 == '' else p1
    p2 = 10000 if p2 == '' else p2
    u1 = 0 if u1 == '' else u1
    u2 = 10000 if u2 == '' else u2
    
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id
            AND (me.price BETWEEN %s AND %s ) AND (me.utility BETWEEN %s AND %s )
            AND me.timeslot_id = 
        (   
            SELECT MAX(timeslot_id) 
            FROM maker_metric WHERE crypto_currency_id = cr.id
        )
        ''' % (p1, p2, u1, u2))
        res = dictfetchall(cursor)
    return res

# get currency detail: id and name cannot be '' neither!
def get_detail(id, name):
    key = 'id' if id != '' else 'name'
    value = id if id !='' else name
    with connection.cursor() as cursor:
        cursor.execute('''SELECT *
        FROM maker_cryptocurrency cr, maker_metric me where cr.id = me.crypto_currency_id AND cr.%s = '%s'
        ORDER BY me.timeslot_id DESC ''' % (key, value))
        res = dictfetchall(cursor)
    return res