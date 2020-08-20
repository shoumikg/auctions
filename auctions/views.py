from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Max

from .models import User,Item, Watchlist, Comment, Bid, Category
from .forms import CreateListingForm, CommentForm, PlaceBid, AddCategory

from datetime import datetime
from django.utils import timezone


def index(request):
    return render(request, "auctions/index.html", {"Items": Item.objects.filter(active=True).order_by('-last_modified')})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def loginRequired(request):
    return render(request, "auctions/login.html", {
                "message": "You need to be logged to access that..."
            })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def items(request,itemID):

    item = get_object_or_404(Item, pk=itemID)
    try:
        watching = Watchlist.objects.get(user=request.user, item = item)
    except Watchlist.DoesNotExist:
        watching = None
    message = None

    if item.bids.all():
        price = item.bids.all().aggregate(Max('amount'))['amount__max']
        bidsplaced = item.bids.all().count()
    else:
        price = item.startingBid
        bidsplaced = 0

    if request.method == 'POST':
        if request.POST.get('watch','')!='': #Add to watchlist
            temp = Watchlist(user=request.user, item = item)
            temp.save()
            watching = True
        if request.POST.get('nowatch','')!='':
            Watchlist.objects.filter(user=request.user, item = item).delete()
            watching = False
        if request.POST.get('close','')!='': #close this item
            item.active = False
            if item.bids.all():
                item.winner = item.bids.filter(amount=price)[0].user
            item.save()
        if request.POST.get('commented','')!='':
            commentform=CommentForm(request.POST)
            if commentform.is_valid():
                newcomment = Comment.objects.create(user = request.user, item = item, content= commentform.cleaned_data['comment'], commentTime=datetime.now())
                newcomment.save()
        if request.POST.get('bid','')!='':
            bidform = PlaceBid(request.POST)
            if bidform.is_valid():
                try:
                    if bidform.cleaned_data['amount']>price:
                        newbid = Bid.objects.create(user = request.user, item = item, amount= bidform.cleaned_data['amount'])
                        newbid.save()
                        price = bidform.cleaned_data['amount']
                        bidsplaced = item.bids.all().count()
                        item.price = price
                        item.last_modified = timezone.localtime()
                        item.save()
                    else:
                        raise ValidationError(_('Bid must be higher than price and positive'))
                except ValidationError:
                    message = "Bid must be higher than price and positive"
            

            
    else:
        #item = get_object_or_404(Item, pk=itemID)
        watchingList = item.starred.all()   
        #watching = None
        #print(watchingList)
        #commentform = CommentForm()

        for entry in watchingList:
            if entry.user == request.user:
                watching = True
                print("Found Harry in watchlist")
                break
            else:
                watching = False

    commentform = CommentForm()
    bidform = PlaceBid()

    comments = item.comments.all().order_by('commentTime')
    #print(comments)

    return render(request, "auctions/item.html", {"Item": item, "Watching": watching, "commentform":commentform, "comments":comments, "price": price, "bidform":bidform, "bidsplaced":bidsplaced, "message":message})


@login_required    
def new(request):

    if request.method == 'POST':
        form = CreateListingForm(request.POST)

        if form.is_valid():
            loggedInUser = request.user
            #newItem = Item(owner=loggedInUser, title=form.cleaned_data['title'], description=form.cleaned_data['description'])#, startingBid=int(form.clean_starting_bid()))
            newItem = Item.objects.create(owner=request.user, title=form.cleaned_data['title'], description=form.cleaned_data['description'], startingBid=form.clean_starting_bid(), winner=request.user, last_modified=timezone.localtime(), category=Category.objects.get(name=request.POST.get('category')), price= form.clean_starting_bid())
            if form.cleaned_data['image']!='':
                newItem.image=form.cleaned_data['image']
            newItem.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        form = CreateListingForm()
    
    context = {'form':form, "Categories":Category.objects.all()}
    return render(request, "auctions/new.html", context)

@login_required
def watch(request):
    watching = request.user.watchlist.all()
    
    return render(request, "auctions/watch.html", {"Watching": watching})

def categories(request):
    message = None
    if request.method == 'POST':
        try:
            temp = Category.objects.create(name=request.POST.get('newcategory'))
            temp.save()
        except IntegrityError:
            message = "Category already exists"

    temp = Category.objects.all()

    context = {"message":message, "Categories":temp}

    return render(request, "auctions/categories.html", context)

def category(request, categoryName):

    temp = get_object_or_404(Category,name=categoryName)

    categoryItems = temp.items.all()
    print(categoryItems)

    context = {"Category":temp, "Items":categoryItems}

    return render(request, "auctions/category.html", context)
    





