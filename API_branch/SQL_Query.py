import sqlite3
from proj.db import connection

# search crypto-currencies based on prefix
def search_by_prefix(pref):
    curren_obj=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE name LIKE %s%%'% [pref]);
    retlist=[];
    for i in curren_obj:
        curtuple=(i.id,i.name,i.logo);
        retlist.append(curtuple);
    return retlist;  #organize all outputs into a tuple list


# sort by price, ascending
def sort_by_price():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY price');
    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;

#sort by volume, descending
def sort_by_volume():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY volume DESC');
    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;


#sort by supply, descending
def sort_by_supply():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY supply DESC');

    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attribute into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;


#sort by utility, descending
def sort_by_utility():
    curren_obj=Metric.objects.raw('SELECT * FROM maker_metric ORDER BY utility DESC');

    idlist=[];
    retlist=[];
    templist=[];
#put all metrics attributes into a temp list
    for i in curren_obj:
        templist.append(i.crypto_currency_id, i.timeslot_id, i.volume, i.privacy, i.price, i.supply, i.utility)
        idlist.append(i.cryoto_currency_id);

#get corresponding names
    for i in range(len(idlist)):
        iter=idlist[i];
        temp=CryptoCurrency.objects.raw('SELECT * FROM maker_cryptocurrency WHERE id=%s' % [iter]);
        namelist.append(temp);

#orgnaize all info into a list ready for return
    for i in range(len(templist)):
        retlist.append(templist[i][0],namelist[i],templist[i][1],templist[i][2],templist[i][3],
        templist[i][4],templist[i][5],templist[i][6]);

    return retlist;

#complicate SQL queries
'''select the currency that
        - in a given time slot (e.g. 12:00 May. 1st), the price > 100
        - and in a given period (e.g. 9:00-15:00 May.1st), average price < 50
< meaning: observe the burst of the currency price>'''
def select_burst_currency(timeslot, period1,period2):

    SELECT name
    FROM maker_cryptocurrency
    WHERE id IN

    (SELECT id FROM maker_cryptocurrency as cr,maker_metric as me WHERE me.timeslot_id=timeslot AND me.price>100 #select the currencies with higher than $100 at the given slot
    INTERSECT
    (SELECT id
    FROM
    (
    SELECT id, avg(price) as p #find currencies in the given period the average price is less than $50
    FROM
    (SELECT id,price FROM maker_metric as me WHERE timeslot BETWEEN period1 AND period2) as temp
    Group By id
    Having p<50) as temp2));

''' select the people 1) who favorites the most popular currencies
        and 2) log in more than 20 times in all
< meaning: find the most active person who likes the most popular, can be a metric of rank$'''
def select_common_active_user():

    SELECT *                                    # give more information about these users
    FROM maker_user
    WHERE
    user_id IN                                  # user_id of users meets the requirement
    (
    SELECT user_id
    FROM
    (
    (SELECT user_id,count(time) as t             #get users log in more than 20 times in all
    FROM maker_log
    Group By user_id
    Having t>20) as table1)

    INTERSECT

    SELECT user_id                              # select user who favorites the most popular currencies
    FROM maker_log
    WHERE cryoto_currency_id IN
    (
    SELECT cryoto_currency_id                   # select the most popular currencies
    FROM
    (
    (SELECT cryoto_currency_id,count(user_id) as ct
    FROM maker_user_favorite
    Group By crypto_currency_id) as curr)
    WHERE ct>=ALL(SELECT ct FROM curr))
    );
