import os, sys, inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tools import load_data, get_data_from_cache, get_tid, get_ts
from preprocessing import *
from threading import Timer
import time
import json
import os

# generate training data from one coin's history
def dataset_from_history(filename, sym):
    # get data from history
    hist_path = os.path.join('..', 'History', 'history_%s.txt' % sym)
    cache = open(hist_path, 'r')
    d1 = json.loads(cache.read())
    data = d1['Data']

    # set output file & header
    file = open(filename, 'w')
    table = 'HistUtility'
    attr = ['open', 'close', 'high', 'low', 'volumeto']
    attr_list = []
    num = 5                 # # previous days used
    for i in range(num):
        for a in attr:
            attr_list.append(a + str(i))
    attr_list.append('next_close')
    write_header(file, table, attr_list)

    # write data into arff
    for k in range(len(data) - 2 * num):
        tmp = ['' for _ in range(len(attr_list))]
        la = len(attr)
        for i in range(num):
            r = data[k + i]
            tmp[la*i] = r['open']
            tmp[la*i + 1] = r['close']
            tmp[la*i + 2] = r['high']
            tmp[la*i + 3] = r['low']
            tmp[la*i + 4] = r['volumeto']
        tmp[ num*la ] = data[k + 2 * num]['close']

        s1 = ""
        i = 0
        for rt in tmp:
            rt = rt if rt is not None else '?'
            if i is not len(attr_list) - 1:
                s1 += '%s, ' % rt
            else: s1 += '%s \n' % rt
            i += 1
        file.write(s1)
    file.close()
    print('%s generated...\n' % filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: python %s [coin symbol]' % sys.argv[0])
        exit(1)
    
    sym = sys.argv[1]
    try:
        os.mkdir('HistSet')
    except OSError:
        pass
    else: pass
    path = os.path.join('HistSet', 'histSet_%s.arff' % sym)
    dataset_from_history(path, sym)