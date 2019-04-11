from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    interest_tag = models.CharField(max_length=200)
    score_of_knowledge = models.FloatField('score of knowledge', null=True, blank=True, default=None)
    # favorite = models.ManyToManyField(CryptoCurrency)       # due many-to-many field, no additional model is needed
    
    def __str__(self):
        return self.email
