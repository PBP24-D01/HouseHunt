from django.shortcuts import render
# from .forms import ReviewEntryForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from HouseHuntAuth.models import Seller
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .forms import *
from django.views.decorators.csrf import csrf_protect
import json
# Create your views here.

@login_required(login_url='/login')
def main_page(request):
    
    return render(request, 'list_penjual.html')

def show_sellers(request):
    data = Seller.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_comment(request, id):
    data = Comment.objects.filter(seller__pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_sellers_by_id(request, id):
    data = Seller.objects.get(id=id)
    data_dict = {
        'id': data.id,
        'company_name': data.company_name,
        'address': data.company_address,
        'phone_number': data.user.phone_number,
        'stars': data.stars,
    }
    return HttpResponse(json.dumps(data_dict), content_type="application/json")


def update_rating(seller):
    comments = Comment.objects.filter(seller=seller)
    rating = comments.aggregate(Avg('star'))['star__avg']
    print(rating)
    seller.stars = round(rating,2)
    seller.save()

@csrf_protect
@login_required(login_url='/login')
def review(request, id):
    seller = get_object_or_404(Seller, id=id)
    comments = Comment.objects.filter(seller_id=id)
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.seller = seller
            if request.user.is_buyer:
                comment.name = request.user.username
            else:
                comment.name = request.user.seller.company_name
            comment.star = request.POST.get('star')
            comment.save()
            
            # Update seller's average rating
            update_rating(seller)
            return redirect('diskusi:review_section', id=id)
    else:
        form = CommentCreateForm()

    context = {
        'seller': seller,
        'comments': comments,
        'form': form,
    }
    return render(request, 'diskusi.html', context)

@csrf_protect
@login_required(login_url='/login')
def reply(request, id):
    comment = get_object_or_404(Comment, id=id)
    seller = comment.seller
    comments = Comment.objects.filter(seller_id=seller.id)
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent_comment = comment
            if request.user.is_buyer:
                reply.name = request.user.username
            else:
                reply.name = request.user.seller.company_name
            reply.save()
            return redirect('diskusi:review_section', id=seller.id)
    else:
        form = ReplyCreateForm()

    context = {
        'seller': seller,
        'comments': comments,
        'form': form,
    }
    return render(request, 'diskusi.html', context)

