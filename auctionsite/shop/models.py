from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class List(models.Model):
    user = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    desc = models.TextField(max_length = 500)       # max length im TextField is unnecessary
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=200, default = None, blank = True, null = True)
    category = models.CharField(max_length=100)
    active_bool = models.BooleanField(default=True) # to perform true or false , empty field is equal to None

class Bids(models.Model):
    user = models.CharField(max_length=100)
    listingid = models.IntegerField()
    bid = models.IntegerField()

class Comments(models.Model):
    user = models.CharField(max_length=100)
    comment = models.TextField()
    listingid = models.IntegerField()

class Watchlist(models.Model):
    watchlist = models.ForeignKey(List, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)