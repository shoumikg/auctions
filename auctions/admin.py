from django.contrib import admin

from .models import User, Item, Comment, Bid, Watchlist, Category

# Register your models here.

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Category)
