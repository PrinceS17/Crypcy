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

def
