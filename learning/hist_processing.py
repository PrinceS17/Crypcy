import os, sys, inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tools import load_data, get_data_from_cache, get_tid, get_ts
from threading import Timer
import time
import json
import os

from .preprocessing import *

# generate training data from one coin's history
def dataset_from_history(filename, sym):
    try:
        os.mkdir('HistSet')
    except OSError:
        pass
    else: pass

    # get data from history
    hist_path = os.path.join('..', 'History', 'history_%s.txt' % sym)
    cache = open(hist_path, 'r')
    d1 = json.loads(cache.read())
    data = d1['Data']

    # set output file & header
    