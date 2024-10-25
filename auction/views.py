from django.shortcuts import render
from django.http import HttpResponse
from .models import Auction

# Create your views here.

def index(request):
    user = request.user
    print(request.user)
    auctions = Auction.objects.all()
    context = {
        "user": user
    }
    return render(request, "index.html", context)

def detail(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    return render(request, "auction/detail.html", {"auction": auction})

def bid(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    auction.current_price += 1000
    auction.save()
    return HttpResponse("Bid success")

def create(request):
    return HttpResponse("Create auction")
