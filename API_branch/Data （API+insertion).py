# This example uses Python 2.7+ and the python-request library
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pymysql
import sqlite3
#import base 64
#class Test(object):
    #def__init__(self,data):
        #self.__dict__=json.loads(data)
conn=sqlite3.connect('proj.db')
#PRAGMA foreign_keys=ON;
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
      'start': '1',
      'limit': '120',
      'convert': 'USD',
      #'sort': 'price',
      #'sort_dir':'desc',
      #'cryptocurrency_type':'coins'
  }
headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '441cb5ae-6618-4110-8db9-df9cba2b05ec',
  }

session = Session()
session.headers.update(headers)

try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      l1=data['data']
      for i in range(len(l1)):

            # get datas for insertion
            ID=l1[i]['id'];
            NAME=l1[i]['name'];
            LOGO=l1[i]['slug'];
            slotid=l1[i]['last_updated']
            supply=l1[i]['circulating_supply']
            dict1=l1[i]['quote']
            dict2=dict1['USD']
            price=dict2['price']
            volume=dict2['volume_24h']


            conn.execute("INSERT OR REPLACE INTO Currencies (CurrencyID,Name,Logo) VALUES(?,?,?)", (ID,NAME,LOGO))
            conn.execute("INSERT OR REPLACE INTO Timeslot (SlotID) VALUES(?)", (slotid,))
            conn.execute("INSERT OR REPLACE INTO Metric (CurrencyID,SlotID,Volume,Price,Circulating_Supply,Utility_Value) VALUES(?,?,?,?,?,NULL)",
            (ID,slotid,volume,price,supply))
      conn.commit();

      #the below lines are for testing
      #cursor = conn.cursor()
      #cursor.execute("SELECT * FROM Metric")
      #print(cursor.fetchall())
      #print('successfully insert');
      conn.close();
      #conn.close();
        #print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
