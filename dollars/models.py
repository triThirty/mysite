from django.db import models
from mongoengine import *
# Create your models here.

class user(models.Model):
    name = StringField()
