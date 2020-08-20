from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

#from .models import Category

from PIL import Image

def validateStartingBid(value):
    if value <= 0:
        raise ValidationError(_('Invalid starting bid'))

def validateNewBid(value):
    if value <= 0:
        raise ValidationError(_('Invalid bid'))

# temp = Category.objects.all()
# Choices = ["Others"]

#  for item in temp:
#      if item.name not in choices:
#          choices.append(item.name)


class CreateListingForm(forms.Form):
    title = forms.CharField(required=True, help_text="Add suitable title for your item to be auctioned", max_length=30)
    description = forms.CharField(required=True, help_text="Add proper description for the item", max_length=140)
    starting_bid = forms.IntegerField(required=True, help_text="Minimum price for which you want this item to be sold", validators=[validateStartingBid])
    image = forms.URLField(required=False, help_text="Provide the URL for a valid image file only...")
    #category = forms.MultipleChoiceField(choices=choices)

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_description(self):
        return self.cleaned_data['description']


    def clean_starting_bid(self):
    #    data =  self.cleaned_data['starting_bid']
    #    if data <= 0:
    #        raise ValidationError(_('Invalid starting bid'))
    #    return data
        return self.cleaned_data['starting_bid']

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=140, help_text="Add your comment here")

    def clean_comment(self):
        return self.cleaned_data['comment']

class PlaceBid(forms.Form):
    amount = forms.IntegerField(help_text="Place a new bid higher than the item's price")

    def clean_amount(self):
        return self.cleaned_data['amount']

class AddCategory(forms.Form):
    name = forms.CharField(max_length="40", help_text="Enter name of new category")

    

