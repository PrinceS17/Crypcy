from django.db import models
from django.utils import timezone
import datetime

'''
Relational Schema: <all IDs and [ , ] are primary keys>

Crypto-Currency (CurrencyID, Name, Logo)
Metric ([Crypto-Currency.CurrencyID, Timeslot.SlotID], Volume, Privacy, Price, Circulating Supply, Utility (Value))
Timeslot (SlotID, Related News. FactID)
User (UserID, Name, Gender, Password, Interest Tag, Score of Knowledge)
Log (LogID, IP, Time, User.UserID, Related News.FactID)
Related News (FactID, Tag, Type, Picture, Content, Author, Slot.SlotID)
Favorite (Crypto-Currency. CurrencyID, User. UserID)

Note: ID is set by django by default.

'''

class RelatedNews(models.Model):
    tag = models.CharField(max_length=200)
    ttype = models.CharField(max_length=200)
    picture = models.URLField()     # in doubt
    content = models.TextField('new content')
    author = models.CharField(max_length=200)
    def __str__(self):
        return self.tag + ': ' + self.content

class Timeslot(models.Model):
    time = models.TimeField('time slot')
    related_news = models.ForeignKey(RelatedNews, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return repr(self.time)

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField()        # in doubt
    time = models.ManyToManyField(Timeslot, 
        through='Metric', 
        through_fields=('crypto_currency', 'timeslot') )
    def __str__(self):
        return self.name
    

class Metric(models.Model):
    crypto_currency = models.ForeignKey(CryptoCurrency, on_delete=models.SET_NULL, null=True)
    timeslot = models.ForeignKey(Timeslot, null=True, on_delete=models.SET_NULL) #, null=True)
    volume = models.PositiveIntegerField()
    privacy = models.FloatField('privacy')     # in doubt, a score, 0-10
    price = models.FloatField('price')
    supply = models.PositiveIntegerField()
    utility = models.FloatField('utility')      # in doubt, a 95.4 like score
    def __str__(self):
        return str(self.timeslot) + ': ' + str(self.crypto_currency)


class User(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    interest_tag = models.CharField(max_length=200)
    score_of_knowledge = models.FloatField('score of knowledge')
    favorite = models.ManyToManyField(CryptoCurrency)       # due many-to-many field, no additional model is needed
    def __str__(self):
        return self.name

class Log(models.Model):
    ip = models.IntegerField()
    time = models.DateTimeField('log-in time')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    related_news = models.ForeignKey(RelatedNews, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self.time) + ' ' + str(self.ip) + ' ' + str(self.user)
