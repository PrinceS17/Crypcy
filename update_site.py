import time, datetime, json, sqlite3, math, random, os, sys, inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from threading import Timer

from maker.models import *
from maker.sql_operation import *
from learning import hist_predict
from maker.basic.SQL_Query import update_utility

# get the latest data from coin market cap, insert into database, & write into history cache
def update_all(time=None):
    time = timezone.now().timestamp() if time is None else time
    print('Loading latest data ... ')
    d1 = load_data(time)    # 1. load data from coin market cap for insertion, cache.txt updated

    print('Loading history to cache ...')
    for r in d1:
        id = r['id']
        sym = r['sym']
        load_history_to_cache(id, sym)      # 2. history cache updated
    hist_predict.main()     # 3. fire a new training, predict cache updated
    
    print('Updating database ...')
    for r in d1:
        tid = generate_timeslot(time)
        mid = (tid % 1e6) * (id % 1e6)
        supply = r['circulating_supply']
        price = r['quote']['USD']['price']
        volume = r['quote']['USD']['volume_24h']
        privacy = 7.0
        with connection.cursor() as cursor:      # 4. database attributes other than utility updated
            cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, crypto_currency_id, timeslot_id) \
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume, privacy, price, supply, id, tid] )
        update_utility(id, sym, price)      # 5. utility updated

def periodical_update(interval):
    update_all()
    update_news_all()
    Timer(interval, periodical_update, [interval]).start()

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cus_crypcy.settings'    # enable updating the database    

