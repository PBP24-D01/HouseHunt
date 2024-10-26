from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rumah.models import House
from .models import Auction, Bid
from .forms import AuctionForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib import messages

# Create your views here.

@login_required(login_url="/login")
def index(request):
    user = request.user
    context = {"user": user}
    return render(request, "index.html", context)

@login_required(login_url="/login")
def detail(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "detail.html", {"auction": auction})


@login_required(login_url="/login")
@csrf_exempt
@require_POST
def bid(request, auction_id):
    if request.user.buyer is None:
        return HttpResponse("You are not a buyer", status=403)

    price = request.POST.get("price")
    auction = Auction.objects.get(id=auction_id)
    
    if auction.is_expired():
        return HttpResponse("Auction is expired", status=400)

    if auction.is_active() is False:
        return HttpResponse("Auction is not active", status=400)
    
    if auction.starting_price >= price:
        return HttpResponse("Bid must be higher than starting price", status=400)

    if auction.highest_buyer == request.user.buyer:
        return HttpResponse("You are the highest bidder", status=400)

    if auction.current_price >= price:
        return HttpResponse("Bid must be higher than current price", status=400)

    bid = Bid(auction=auction, buyer=request.user.buyer, price=price)
    bid.save()
    return HttpResponse("Bid success", status=201)


@login_required(login_url="/login")
@csrf_exempt
def create_auction(request):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)

    form = AuctionForm(request.POST or None)
    houses = House.objects.filter(seller=request.user.seller)
    form.fields["house"].queryset = houses
    if request.method == "POST":
        if form.is_valid() and form.clean():
            auction = form.save(commit=False)
            auction.seller = request.user.seller
            auction.save()
            messages.success(request, "Your auction successfully created!")
            return HttpResponseRedirect("/auctions/")
        else:
            return HttpResponse(f"Invalid data: {form.errors}", status=400)

    return render(request, "create.html", {"form": form, "title" : "Create Auction"})

@login_required(login_url="/login")
@csrf_exempt
def edit_auction(request, auction_id):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)
    
    auction = Auction.objects.get(pk=auction_id)
    
    if auction.seller != request.user.seller:
        return HttpResponse("You are not the seller of this auction", status=403)
    
    if request.method == "POST":
        form = AuctionForm(request.POST, instance=auction)
        if form.is_valid() and form.clean():
            auction = form.save(commit=False)
            auction.seller = request.user.seller
            auction.save()
            return HttpResponseRedirect("/auctions/")
        else:
            return HttpResponse(f"Invalid data: {form.errors}",)

    return render(request, "create.html", {"form": form, "title" : "Edit Auction"})

@login_required(login_url="/login")
def delete_auction(request, auction_id):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)
    
    auction = Auction.objects.get(id=auction_id)
    
    if auction.seller != request.user.seller:
        return HttpResponse("You are not the seller of this auction", status=403)
    
    if auction.is_active():
        return HttpResponse("Auction is still active", status=400)
    
    auction.delete()
    return HttpResponseRedirect("/auctions/")

def get_all_auctions(request):
    auctions = Auction.objects.all()
    return HttpResponse(serializers.serialize("json", auctions), content_type="application/json")