from django.db import connection
from .sql_operation import dictfetchall

'''
    select the currency that
        - in a given time slot (e.g. 12:00 May. 1st), the price > a
        - and in a given period (e.g. 9:00-15:00 May.1st), average price < b
    < meaning: observe the burst of the currency price>
    arguments: tid1, price1, tid21, tid22, price2
    [in demo, since price doesn't vary, t21 > t22 will return []. ]
'''
def get_burst_currency(t1, t21, t22, price1, price2):
    query1 = '''SELECT DISTINCT *
    FROM maker_cryptocurrency NATURAL JOIN
    (
        SELECT crypto_currency_id AS id, price
        FROM maker_metric
        WHERE timeslot_id = %s AND price > %s
     INTERSECT
        SELECT m1.crypto_currency_id AS id, m1.price
        FROM maker_metric m1
        WHERE (
            SELECT AVG(price)
            FROM maker_metric m2
            WHERE m1.crypto_currency_id = m2.crypto_currency_id AND timeslot_id BETWEEN %s AND %s
            GROUP BY m2.crypto_currency_id
        ) < %s
    )''' % (t1, price1, t21, t22, price2)

    with connection.cursor() as cursor:
        cursor.execute(query1)
        res = dictfetchall(cursor)
    return res

''' 
    select the currency that 
        - price < 1
        - has the highest average utility (among that whose price < 1).
    <meaning: give an advice on currency of best utility given budget.>
    arguments: price (budget)
'''
def get_efficient_currency(price):
    query2 = '''SELECT id, name, utility
    FROM maker_cryptocurrency NATURAL JOIN
    (
        SELECT DISTINCT m.crypto_currency_id AS id, m.utility, m.timeslot_id 
        FROM maker_metric m
        WHERE price < %s AND (
            SELECT AVG(m1.utility)
            FROM maker_metric m1
            WHERE m.crypto_currency_id = m1.crypto_currency_id
            GROUP BY m1.crypto_currency_id
        
        ) >= 
        (
            SELECT MAX(ut_avg)
            FROM
            (
                SELECT AVG(utility) AS ut_avg
                FROM maker_metric
                WHERE price < %s
                GROUP BY crypto_currency_id
            )
        )
        ORDER BY timeslot_id DESC LIMIT 1
    ) ''' % (price, price)

    with connection.cursor() as cursor:
        cursor.execute(query2)
        res = dictfetchall(cursor)
    
    return res

'''
    Interesting select 1: choose the coin of highest utility currently 
    among those that contains a given name, say, "coin".    -- Song
'''
def get_best_coin_by_name(name):
    query = '''SELECT DISTINCT c.id, c.name, m.timeslot_id, m.price, m.utility  
    FROM maker_cryptocurrency c JOIN maker_metric m ON c.id = m.crypto_currency_id
    WHERE name LIKE '%%%s%%' AND m.timeslot_id = 
    (   
        SELECT DISTINCT timeslot_id 
        FROM maker_metric ORDER BY timeslot_id DESC LIMIT 1
    )
    ORDER BY utility DESC''' % (name)

    with connection.cursor() as cursor:
        cursor.execute(query)
        res = dictfetchall(cursor)

    return res

'''
    Interesting select 2: select the related news that contains the given
    word or sentence and list the timeslots when it appears.
    Currently also shows repeated contents at first, and allow time to be 
    null.   -- Song
'''
def get_news_by_word(word):
    query = '''SELECT r.content, t.id, t.time
    FROM maker_relatednews r LEFT OUTER JOIN maker_timeslot t ON t.related_news_id = r.id
    WHERE r.content LIKE '%%%s%%' ORDER BY t.id DESC''' % (word)
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        res = dictfetchall(cursor)

    return res

# End. -- Song
