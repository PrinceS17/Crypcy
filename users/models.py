from django.db import models
from django.contrib.auth.models import AbstractUser
from maker.models import CryptoCurrency

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    interest_tag = models.CharField(max_length=200, null=True, blank=True)
    score_of_knowledge = models.FloatField('score of knowledge', null=True, blank=True, default=None)
    favorite = models.ManyToManyField(CryptoCurrency, blank=True)       # due many-to-many field, no additional model is needed
    
    def __str__(self):
        return self.email
