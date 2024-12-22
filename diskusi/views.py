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
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
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

def show_reply(request, id):
    data = Reply.objects.filter(parent_comment__pk=id)
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
    if comments.exists():
        rating = comments.aggregate(Avg('star'))['star__avg']
    else:
        rating = 0
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

@csrf_exempt
def add_comment_api(request,id):
    seller = get_object_or_404(Seller, id=id)
    author = seller.user
    form = CommentCreateForm(request.POST)
    print(request.POST)
    if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = author
                comment.seller = seller
                if request.user.is_buyer:
                    comment.name = request.user.username
                else:
                    comment.name = request.user.seller.company_name
                comment.star = request.POST.get('star')
                comment.save()
                # Update seller's average rating
                update_rating(comment.seller)
                return JsonResponse({'status': 'success', 'message': 'Comment added successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

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
            reply.name = seller.company_name
            reply.save()
            return JsonResponse({'redirect_url': reverse('diskusi:review_section', args=[seller.id])})
    else:
        form = ReplyCreateForm()

    context = {
        'comment': comment,
        'seller': seller,
        'comments': comments,
        'form': form,
    }
    return render(request, 'reply.html', context)

@login_required(login_url='/login')
@csrf_protect
def delete_comment(request, id):
    try:
        comment = get_object_or_404(Comment, pk=id)
        comment.delete()
        return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
@login_required(login_url='/login')
@csrf_protect
def delete_reply(request, id):
    try:
        reply = get_object_or_404(Reply, id=id)
        reply.delete()
        return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_protect
@login_required(login_url='/login')
def edit_comment(request, id):
    comment = Comment.objects.get(pk = id)

    form = CommentCreateForm(request.POST or None, instance=comment)

    if form.is_valid() and request.method == "POST":
        comment = form.save(commit=False)
        comment.author = request.user
        comment.seller = comment.seller
        if request.user.is_buyer:
            comment.name = request.user.username
        else:
            comment.name = request.user.seller.company_name
        comment.star = request.POST.get('star')
        comment.save()
        return JsonResponse({'redirect_url': reverse('diskusi:review_section', args=[comment.seller.id])})

    context = {'form': form,
               'comment':comment}
    return render(request, "edit.html", context)

@csrf_protect
@login_required(login_url='/login')
def edit_reply(request, id):
    reply = get_object_or_404(Reply, id=id)
    seller = reply.comment.seller
    comments = Comment.objects.filter(seller_id=seller.id)
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.name = seller.company_name
            reply.save()
            return JsonResponse({'redirect_url': reverse('diskusi:review_section', args=[seller.id])})
    else:
        form = ReplyCreateForm(None,instance=reply)

    context = {
        'reply': reply,
        'comments': comments,
        'form': form,
    }
    return render(request, 'reply.html', context)

#flutter
@csrf_exempt
def reply_api(request, id):
    comment = get_object_or_404(Comment, id=id)
    seller = comment.seller
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent_comment = comment
            reply.name = seller.company_name
            reply.save()
            return JsonResponse({'status': 'success', 'message': 'Reply added successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def delete_comment_api(request, id):
    if request.method == 'POST':
        try:
            comment = get_object_or_404(Comment, pk=id)
            seller = comment.seller
            comment.delete()
            update_rating(seller)
            return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def delete_reply_api(request, id):
    if request.method == 'POST':
        try:
            reply = get_object_or_404(Reply, id=id)
            reply.delete()

            return JsonResponse({'status': 'success', 'message': 'Reply deleted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def edit_comment_api(request, id):
    comment = get_object_or_404(Comment, pk=id)
    if request.method == 'POST':
        form = CommentCreateForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.seller = comment.seller
            if request.user.is_buyer:
                comment.name = request.user.username
            else:
                comment.name = request.user.seller.company_name
            comment.star = request.POST.get('star')
            comment.save()
            update_rating(comment.seller)
            return JsonResponse({'status': 'success', 'message': 'Comment edited successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def edit_reply_api(request, id):
    reply = get_object_or_404(Reply, id=id)
    seller = reply.parent_comment.seller
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.name = seller.company_name
            reply.save()
            return JsonResponse({'status': 'success', 'message': 'Reply edited successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

