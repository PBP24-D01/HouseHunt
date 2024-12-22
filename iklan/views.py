from django.shortcuts import render, redirect, reverse
from iklan.forms import IklanEntryForm
from iklan.models import IklanEntry
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.core.serializers import serialize
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags 
from django.http import HttpResponseForbidden
from rumah.models import House
import json


@login_required
def show_iklan(request):
    if request.user.seller is None:
        return HttpResponseForbidden("Hanya penjual yang bisa mengakses")
    
    iklan = IklanEntry.objects.filter(seller=request.user.seller)

    context = {
        'iklan' : iklan,
    }
    return render(request, 'iklan.html', context)

@login_required
def create_iklan(request):
    form = IklanEntryForm(request.POST or None, request.FILES)
    houses = House.objects.filter(seller=request.user.seller)

    if form.is_valid() and request.method == "POST":
        IklanEntry = form.save(commit=False)
        IklanEntry.seller = request.user.seller
        IklanEntry.save()
        return redirect('iklan:show_iklan')
    
    context = {'form': form, 'houses': houses}    
    return render(request, "create_iklan.html", context)

@login_required
def edit_iklan(request, id_rumah):
    iklan = IklanEntry.objects.get(pk = id_rumah)

    form = IklanEntryForm(request.POST or None, request.FILES or None, instance=iklan)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('iklan:show_iklan'))

    context = {'form': form}
    return render(request, "edit_iklan.html", context)

@login_required
def delete_iklan(request, id_rumah):
    iklan = IklanEntry.objects.get(pk = id_rumah)
    iklan.delete()
    return HttpResponseRedirect(reverse('iklan:show_iklan'))

def show_xml(request):
    data = IklanEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id_rumah):
    data = IklanEntry.objects.filter(pk=id_rumah)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
@require_POST
def add_iklan_ajax(request):
    rumah = strip_tags(request.POST.get("rumah"))
    start_date = strip_tags(request.POST.get("start_date"))
    end_date = strip_tags(request.POST.get("end_date"))
    banner = request.FILES.get("banner")
    house = House.objects.get(pk=rumah)
    print(banner)
    new_iklan = IklanEntry(
        rumah=house,
        start_date=start_date,
        end_date=end_date,
        banner=banner,
        seller=request.user.seller
    )
    new_iklan.save()

    return JsonResponse({"success": True})  

@login_required(login_url='/login')
def iklan_json(request):
    if not request.user.is_seller:
        return JsonResponse({'error': 'Hanya Penjual yang bisa mengakses.'}, status=403)

    iklan = IklanEntry.objects.filter(seller=request.user.seller)

    iklan_data = []
    for i in iklan:
        gambar_url = i.rumah.gambar.url if i.rumah.gambar else None
        banner_url = i.banner.url if i.banner else None
        
        iklan_data.append({
            'seller': i.seller.user.username,  
            'rumah_id': i.rumah.id,
            'judul': i.rumah.judul,
            'deskripsi': i.rumah.deskripsi,
            'harga': i.rumah.harga,
            'lokasi': i.rumah.lokasi,
            'gambar': gambar_url,
            'kamar_tidur': i.rumah.kamar_tidur,
            'kamar_mandi': i.rumah.kamar_mandi,
            'start_date': i.start_date.isoformat(),  
            'end_date': i.end_date.isoformat(),   
            'created_at': i.created_at.isoformat(), 
            'updated_at': i.updated_at.isoformat(), 
            'banner': banner_url,
        })
    
    return JsonResponse({'iklan': iklan_data}, status=200)

@login_required
def create_iklan_flutter(request):
    if request.method == "POST":
        form = IklanEntryForm(request.POST or None, request.FILES)
        
        if form.is_valid():
            IklanEntry = form.save(commit=False)
            IklanEntry.seller = request.user.seller
            IklanEntry.save()
            houses = House.objects.filter(seller=request.user.seller)

            response_data = {
                'status': 'success',
                'message': 'Iklan created successfully',
                'iklan_id': IklanEntry.id,
                'houses': list(houses) 
            }
            return JsonResponse(response_data, status=201)
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }
            return JsonResponse(response_data, status=400)
    response_data = {
        'status': 'error',
        'message': 'Invalid request method'
    }
    return JsonResponse(response_data, status=405)


@login_required
def edit_iklan_flutter(request, id_rumah):
    try:
        iklan = IklanEntry.objects.get(id=id_rumah, seller=request.user.seller)
    except IklanEntry.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Iklan item not found"}, status=404)

    if request.method == 'POST':
        form = IklanEntryForm(request.POST, request.FILES, instance=iklan)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Iklan item updated successfully"}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data", "errors": form.errors}, status=400)

    form_data = {
        'start_date': iklan.start_date,
        'end_date': iklan.end_date,
        'banner': iklan.banner,
    }
    return JsonResponse({"status": "success", "form_data": form_data}, status=200)

@login_required(login_url='/login')
def delete_iklan_flutter(request, id_rumah):
    try:
        iklan = IklanEntry.objects.get(rumah__id=id_rumah, seller=request.user.seller)
        iklan.delete()
        return JsonResponse(
            {"status": "success", "message": "Iklan item deleted successfully"},
            status=200
        )
    except IklanEntry.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Iklan item not found"},
            status=404
        )