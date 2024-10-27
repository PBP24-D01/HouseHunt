from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rumah.models import House
from .models import Auction, Bid
from .forms import AuctionForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


@login_required(login_url="/login")
def index(request):
    user = request.user
    context = {"user": user}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def detail(request, auction_id):
    context = {"auction": get_auction_by_id(request, auction_id, False), "user": request.user}
    return render(request, "detail.html", context)


@login_required(login_url="/login")
@csrf_exempt
@require_POST
def bid(request, auction_id):
    if request.user.buyer is None:
        return HttpResponse("You are not a buyer", status=403)

    price = int(request.POST.get("price"))
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
    messages.success(request, "Your bid has been placed!")
    return HttpResponse("Bid success", status=201)


@login_required(login_url="/login")
@csrf_exempt
def create_auction(request):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)

    form = AuctionForm(request.POST or None)
    houses = House.objects.filter(seller=request.user.seller)
    valid_house = House.objects.filter(
        id__in=[
            house.id
            for house in houses
            if len(Auction.objects.filter(house=house)) == 0
        ]
    )
    form.fields["house"].queryset = valid_house
    if request.method == "POST":
        if form.is_valid() and form.clean():
            auction = form.save(commit=False)
            auction.seller = request.user.seller
            auction.current_price = auction.starting_price
            auction.save()
            messages.success(request, "Auction successfully created!")
            return HttpResponseRedirect("/auction/")
        else:
           messages.error(request, f"Invalid data")

    return render(request, "create.html", {"form": form, "title": "Create Auction"})


@login_required(login_url="/login")
@csrf_exempt
def edit_auction(request, auction_id):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)

    auction = Auction.objects.get(pk=auction_id)

    if auction.seller != request.user.seller:
        return HttpResponse("You are not the seller of this auction", status=403)

    form = AuctionForm(request.POST or None, instance=auction)
    if request.method == "POST":
        if form.is_valid() and form.clean():
            auction = form.save(commit=False)
            auction.seller = request.user.seller
            auction.save()
            messages.success(request, "Auction successfully edited!")
            return HttpResponseRedirect("/auction/")
        else:
            messages.error(request, f"Invalid data")

    return render(request, "create.html", {"form": form, "title": "Edit Auction"})
    

@login_required(login_url="/login")
def delete_auction(request, auction_id):
    if request.user.seller is None:
        return HttpResponse("You are not a seller", status=403)
    
    if request.method != "DELETE":
        return HttpResponse("Method not allowed", status = 405)

    auction = Auction.objects.get(id=auction_id)

    if auction.seller != request.user.seller:
        return HttpResponse("You are not the seller of this auction", status=403)

    if auction.is_active():
        return HttpResponse("Auction is still active", status=400)

    auction.delete()
    return HttpResponseRedirect(f"/auction/")


def get_all_auctions(request):
    auctions = Auction.objects.all()
    auctions_json = []
    for auction in auctions:
        house = House.objects.get(pk=auction.house.id)
        auctions_json.append(
            {
                "id": auction.id,
                "title": auction.title,
                "house_url": f"/house/{house.pk}",
                "house_title": house.judul,
                "house_address": house.lokasi,
                "house_image": house.gambar.url,
                "house_price": house.harga,
                "start_date": auction.start_date.strftime("%H:%M:%S %d-%m-%Y"),
                "end_date": auction.end_date.strftime("%H:%M:%S %d-%m-%Y"),
                "starting_price": auction.starting_price,
                "current_price": auction.current_price,
                "highest_buyer": (
                    auction.highest_buyer.user.username
                    if auction.highest_buyer is not None
                    else None
                ),
                "seller": auction.seller.user.username,
                "created_at": auction.created_at,
                "updated_at": auction.updated_at,
                "is_active": auction.is_active(),
                "is_expired": auction.is_expired(),
            }
        )

    return JsonResponse(auctions_json, safe=False)


def get_auction_by_id(request, auction_id, json=True):
    auction = Auction.objects.get(id=auction_id)
    house = House.objects.get(pk=auction.house.id)
    auction_json = {
        "id": auction.id,
        "title": auction.title,
        "house_url": f"/house/{house.pk}",
        "house_title": house.judul,
        "house_address": house.lokasi,
        "house_image": house.gambar.url,
        "house_description": house.deskripsi,
        "house_price": house.harga,
        "start_date": auction.start_date.strftime("%H:%M:%S %d-%m-%Y"),
        "end_date": auction.end_date.strftime("%H:%M:%S %d-%m-%Y"),
        "starting_price": auction.starting_price,
        "current_price": auction.current_price,
        "highest_buyer": (
            auction.highest_buyer.user.username
            if auction.highest_buyer is not None
            else None
        ),
        "seller": auction.seller.user.username,
        "created_at": auction.created_at,
        "updated_at": auction.updated_at,
        "is_active": auction.is_active(),
        "is_expired": auction.is_expired(),
    }

    if json:
        return JsonResponse(auction_json, safe=False)
    return auction_json