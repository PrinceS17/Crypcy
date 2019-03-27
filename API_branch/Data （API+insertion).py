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
#print("open successfully!")
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

            ID=l1[i]['id'];
            #print(ID)
            #print()
            NAME=l1[i]['name'];
            LOGO=l1[i]['slug'];
            #print(l1[i])
            conn.execute("INSERT OR REPLACE INTO Currencies (CurrencyID,Name,Logo) VALUES(?,?,?)", (ID,NAME,LOGO))
      conn.commit();

      #cursor = conn.cursor()
      #cursor.execute("SELECT * FROM Currencies")
      #print(cursor.fetchall())
      #print('successfully insert');
      conn.close();
      #conn.close();
        #print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
