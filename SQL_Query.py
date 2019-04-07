Begin Simple SQl Queries
@author Ruixin Zou

import sqlite3
from proj.db import connection

# search crypto-currencies based on prefix
# prefix: pref
def search_by_prefix(pref):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM maker_cryptocurrency cr where cr.name LIKE "%s%%" ''' % pref)

    res=dictfetchall(cursor)
    return res


# sort by price, ascending
def sort_by_price():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT cr.logo, cr.id, cr.name, me.price, me.volume, me.supply,me.utility FROM maker_cryptocurrency cr, maker_metric me where cr.id=
        me.crypto_currency_id
        ORDER BY price''')

    res=dictfetchall(cursor)
    return res

#sort by volume, descending
def sort_by_volume():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT cr.logo, cr.id, cr.name, me.price, me.volume, me.supply,me.utility FROM maker_cryptocurrency cr, maker_metric me where cr.id=
        me.crypto_currency_id
        ORDER BY volume DESC''')

    res=dictfetchall(cursor)
    return res


#sort by supply, descending
def sort_by_supply():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT cr.logo, cr.id, cr.name, me.price, me.volume, me.supply,me.utility FROM maker_cryptocurrency cr, maker_metric me where cr.id=
        me.crypto_currency_id
        ORDER BY supply DESC''')

    res=dictfetchall(cursor)
    return res


#sort by utility, descending
def sort_by_utility():
    with connection.cursor() as cursor:
        cursor.execute('''SELECT cr.logo, cr.id, cr.name, me.price, me.volume, me.supply,me.utility FROM maker_cryptocurrency cr, maker_metric me where cr.id=
        me.crypto_currency_id
        ORDER BY utility DESC''')

    res=dictfetchall(cursor)
    return res

#----end Ruixin Zou
