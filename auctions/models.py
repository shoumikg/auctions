from django.contrib.auth.models import AbstractUser
from django.db import models

from PIL import Image
from datetime import datetime

from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=25)

def default_Category():
    return Category.objects.get_or_create(name="Others")

class Item(models.Model):
    owner = models.ForeignKey('auctions.User', on_delete=models.CASCADE, related_name="owners") #That is a bad related name. Don't think I have actually used it. But still won't risk breaking things by deleting it.
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=140)
    startingBid = models.IntegerField(help_text="Add starting bid in", default=100)
    winner = models.ForeignKey('auctions.User', on_delete=models.CASCADE) #add related name later if needed
    image = models.URLField(max_length=200, default="https://elitescreens.com/images/product_album/no_image.png")
    last_modified = models.DateTimeField(default=timezone.localtime)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('auctions.Category', on_delete=models.CASCADE, related_name="items", default=default_Category) #this will give us all the items present in a certain category. We can then use it for "items in this category" page.
    price = models.IntegerField(default=startingBid)

class Comment(models.Model):
    user = models.ForeignKey('auctions.User', on_delete=models.CASCADE)
    item = models.ForeignKey('auctions.Item', on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=140)
    commentTime = models.DateTimeField(default=timezone.localtime)

    def commentedAt(self):
        return self.commentTime

class Bid(models.Model):
    user = models.ForeignKey('auctions.User', on_delete=models.CASCADE)
    item = models.ForeignKey('auctions.Item', on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField(help_text="Add your bid")
    
class Watchlist(models.Model):
    user = models.ForeignKey('auctions.User', on_delete=models.CASCADE, related_name="watchlist")
    item = models.ForeignKey('auctions.Item', on_delete=models.CASCADE, related_name="starred")
