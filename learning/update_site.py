import time, datetime, json, sqlite3, math, random, os, sys, inspect
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cus_crypcy.settings'    # enable updating the database    

from django.http import HttpResponse
from django.db import connection
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from threading import Timer

from tools import *
import hist_predict
from hist_predict import *

blacklist = [2955, 3144, 2335, 2471]

# get the latest data from coin market cap, insert into database, & write into history cache
def update_all(time=None):
    global blacklist
    
    # ------------- Stage 1, Choice 1: Load data from api and process --------------- # 
    print('Loading latest data ... ')
    d1 = load_data(time)    # 1. load data from coin market cap for insertion, cache.txt updated

    print('Loading history to cache ...')
    for r in d1:
        id = r['id']
        sym = r['symbol']
        load_history_to_cache(id, sym)      # 2. history cache updated
        print(' - history of coin', sym, 'loaded to cache...')
    
    try:
        jvm.start(system_cp=True, packages=True, max_heap_size='512m')   
        hist_predict.main()     # 3. fire a new training, predict cache updated
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
    
    # --------------- Stage 1, Choice 2: Get data from cache  ------------------------ #
    # d1 = get_data_from_cache()

    # --------------- Stage 2: Update database using data obtained ------------------- # 
    print('Updating database ...')
    option = 1
    if option == 1:      # 1. manually insert all history
        insert_all_history()
        for r in d1:
            id = r['id']
            sym = r['symbol']
            if id in blacklist: continue
            price = r['quote']['USD']['price']
            update_utility(id, sym, price)
            print(' - utility of coin', sym, 'updated...')

    elif option == 2:    # 2. automatically update 1 at a time
        for r in d1:
            id = r['id']
            sym = r['symbol']
            if id in blacklist: continue
            time = timezone.now().timestamp() if time is None else time
            tid = generate_timeslot(time)
            mid = (tid % 1e6) * (id % 1e6)
            supply = r['circulating_supply']
            price = r['quote']['USD']['price']
            volume = r['quote']['USD']['volume_24h']
            privacy = 7.0
            with connection.cursor() as cursor:      # 4. database attributes other than utility updated
                cursor.execute("INSERT OR REPLACE INTO maker_metric (id, volume, privacy, price, supply, utility, crypto_currency_id, timeslot_id) \
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", [mid, volume, privacy, price, supply, 0.01, id, tid] )
            update_utility(id, sym, price)      # 5. utility updated

ii = 0
def periodical_update(interval):
    update_all()
    # update_news1()        # light debug
    global ii
    print('Update No.', ii)
    ii += 1
    Timer(interval, periodical_update, [interval]).start()

# patch for volume
def correct_volume():
    print('Correcting wierd volume...')
    fix_list = [1, 2, 52, 131, 328, 512, 825, 1027, 1720, 1765, 1831, 1839, 1958, 2010, 2011, 3602]
    d = get_data_from_cache()
    for r in d:
        id = r['id']
        if id not in fix_list: continue
        sym = r['symbol']
        supply = r['circulating_supply']
        price = r['quote']['USD']['price']
        # with connection.cursor() as cursor:
        #     cursor.execute("DELETE FROM maker_metric WHERE crypto_currency_id = %s AND privacy = 7.0", [id])
        # load_history_from_cache(id, sym, supply)
        update_utility(id, sym, price)

def main():
    periodical_update(3600 * 24)        # unit: s

if __name__ == "__main__":
    main()
    # correct_volume()          # need figuring out reason