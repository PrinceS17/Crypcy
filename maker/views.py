from django.http import HttpResponse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import json
import sqlite3
# import sql_operation

from .sql_operation import *

def index(request):

    # d = load_data()
    d = get_data_from_cache()
    update_news('init', 'hihi', 'http://images.firstcovers.com/covers/flash/f/final_exams-1558705.jpg?i', \
            'Hello World!', 'Trump')
    update_timeslot()
    update_currency(id=1)
    tmp = d[2]['name']
    delete_currency(name='Bitcoin')
    if not delete_currency(id=1):
        print('2nd delete failed. Test passed.')
    
    return HttpResponse("Hello, world. You're at the maker index. Bitcoin is: %s" % tmp)