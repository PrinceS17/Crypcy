import os, sys, inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tools import load_data, get_data_from_cache, get_tid, get_ts
from threading import Timer
import time
import json
import os

''' 
    Begin: periodical load data, and ARFF generation script. 
        [Modified from Data_processing.py (Zou)]

    Advance function 2:
    Based on the real-time price, supply and other data, try to predict the recent 
    value (average price of next interval). Consists of 2 parts: real-time gathering
    and preprocessing, offline-training (for now) and model update.     -- Song
'''

# periodical load data: schedule load events here (interval in hour)
def periodical_load(t1, interval):
    # t1 = str(get_ts() - interval)
    t2 = str(get_ts())
    load_data(t2)
    periodical_load.cnt += 1
    if periodical_load.cnt > 1:
        path = os.path.join('Dataset', 'dataset_%s-%s.arff' % (t1, t2))
        generate_training_file(path, t1, t2)
    Timer(interval, periodical_load, [t2, interval]).start()

periodical_load.cnt = 0

# write ARFF header
def write_header(file, table, attribute):
    file.write('@RELATION %s\n' % table)
    for attr in attribute:
        file.write('@ATTRIBUTE %s NUMERIC\n' % attr)
    file.write('\n@DATA\n')

# get training data by reading from 2 cache file with t1 & t2
def generate_training_file(filename, t1, t2):
    try: os.mkdir('Dataset')
    except OSError: pass
    else: pass

    file = open(filename, 'w')
    table = 'Utility'
    attribute = ['circulating_supply', 'total_supply', 'max_supply','price', 'volume', 'percent_change_1h', \
        'percent_change_24h', 'percent_change_7d', 'mkt_cap', 'next price']
    write_header(file, table, attribute)

    # write data
    d1 = get_data_from_cache(t1)
    d2 = get_data_from_cache(t2)
    for i in range(min(len(d1), len(d2))):
        tmp1 = [0 for _ in range(len(attribute))]
        tmp = ['' for _ in range(len(attribute))]
        tmp1[0] = d1[i]['circulating_supply'], 
        tmp1[1] = d1[i]['total_supply'], 
        tmp1[2] = d1[i]['max_supply'], 
        tmp1[3] = d1[i]['quote']['USD']['price'], 
        tmp1[4] = d1[i]['quote']['USD']['volume_24h'], 
        tmp1[5] = d1[i]['quote']['USD']['percent_change_1h'], 
        tmp1[6] = d1[i]['quote']['USD']['percent_change_24h'], 
        tmp1[7] = d1[i]['quote']['USD']['percent_change_7d'], 
        tmp1[8] = d1[i]['quote']['USD']['market_cap'], 
        tmp1[9] = d2[i]['quote']['USD']['price']

        s1 = ""
        for j in range(len(attribute)):
            if type(tmp1[j]) == tuple: 
                tmp[j] = str(tmp1[j][0]) if tmp1[j][0] is not None else '?'  # deal with missing values
            elif type(tmp1[j]) == float:
                tmp[j] = str(tmp1[j]) if tmp1[j] is not None else '?' 
            if j is not len(attribute) - 1: 
                s1 += '%s, ' % tmp[j]
            else: s1 += '%s \n' % tmp[j]
        file.write(s1)

    file.close()
    print('%s generated...\n' % filename)


if __name__ == "__main__":
    t1 = str(get_ts())
    if len(sys.argv) != 2:
        print('Usage: python %s [interval in second]' % sys.argv[0])
        exit(1)
    interval = int(sys.argv[1])
    periodical_load(t1, interval)      # interval: in second


'''
    End. -- Song
'''