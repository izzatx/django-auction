from django.shortcuts import render,redirect
from .models import *
from django.template import loader
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


from django.http import JsonResponse

# Create your views here.

def index(request):
    list_objects = List.objects.all()  

    return render(request,'shop/index.html',
                  {'list_objects': list_objects.filter(active_bool = True),
                   })


# this is for me to test the layout or base for the html 
def base(request):
    template = loader.get_template('shop/base.html')
    context = {

    }
    return HttpResponse(template.render(context,request))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Welcome {username} !")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'shop/register.html',{'form':form})


def category(request):
    category = List.objects.values('category').distinct()
    return render(request, "shop/category.html",{"category" : category,})

def cat_view(request, category_name):
    category = List.objects.filter(category = category_name)
    return render(request, "shop/index.html",{"list_objects" : category,}) # context mesti sama dengan index.html


@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    context = { 
        'watchlist' : watchlist
    }
    return render(request,'shop/watchlist.html',context)

def addtowatchlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = List.objects.get(id=prod_id)
            if(product_check):
                if(Watchlist.objects.filter(user=request.user, watchlist_id = prod_id)):
                    return JsonResponse({'status':"Product already in watchlist"})
                else:
                    Watchlist.objects.create(user=request.user, watchlist_id = prod_id) # watchlist_id is variable created from models.py (inherit from watch_list)
                    return JsonResponse({'status':"Product added to watchlist"})
            else:
                return JsonResponse({'status':"No such product found"})

        else:
            return JsonResponse({'status':"Login to continue"})
    return redirect('/')

def deletewatchlistitem(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            
            if(Watchlist.objects.filter(user=request.user, watchlist_id = prod_id)):
                watchlistitem = Watchlist.objects.get(user=request.user, watchlist_id = prod_id)
                watchlistitem.delete()
                return JsonResponse({'status':"Product removed from watchlist"})
            else:
                return JsonResponse({'status':"Product not found in watchlist"})
        else:
            return JsonResponse({'status':"Login to continue"})

    return redirect('/')


def minbid(min_bid,present_bid):
    for bid_list in present_bid:
        if min_bid < int(bid_list.bid):
            min_bid = int(bid_list.bid)
    return min_bid


@login_required
def bid(request):
    bid_amount = request.GET["bid_amount"]
    place_bidid = request.GET["place_bidid"]
    latest_bid = Bids.objects.filter(listingid = place_bidid)
    start_bid = List.objects.get(pk = place_bidid)
    min_req_bid = start_bid.starting_bid
    min_req_bid = minbid(min_req_bid,latest_bid)

    if int(bid_amount) > int(min_req_bid):
        mybid = Bids(user = request.user.username, listingid = place_bidid , bid = bid_amount)
        mybid.save()
        messages.success(request, "Bid Placed")
        # return redirect("index")
        return listing(request, place_bidid)



    messages.warning(request, f"Sorry, {bid_amount} is less. It should be more than {min_req_bid}$.")
    return listing(request, place_bidid)

def listing(request,id):
    list = List.objects.get(pk=id, active_bool = True)
    latest_bid = Bids.objects.filter(listingid = id)
    context = {
        "list" : list,
        "latest_bid" : minbid(list.starting_bid,
                              latest_bid),
    } 
    return render(request,'shop/listing.html',context)

@login_required
def winning(request):
    return render(request,'shop/winning.html')

@login_required
def create(request):
    if request.method == "POST":
        create = List()
        create.user = request.user.username
        create.title = request.POST["create_title"]
        create.desc = request.POST["create_desc"]
        create.starting_bid = request.POST["create_initial_bid"]
        create.image_url = request.POST["image_url"]
        create.category = request.POST["category"]
        # m = auctionlist(title = title, desc=desc, starting_bid = starting_bid, image_url = image_url, category = category)
        create.save()
        return redirect("index")
    return render(request,'shop/create.html')

