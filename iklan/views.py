from django.shortcuts import render, redirect, reverse
from iklan.forms import IklanEntryForm
from iklan.models import IklanEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
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

@login_required
def show_iklan(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Hanya penjual yang bisa mengakses")
    
    iklan = IklanEntry.objects.filter(user=request.user)

    context = {
        'iklan' : iklan,
    }
    return render(request, 'iklan.html', context)

@login_required
def create_iklan(request):
    form = IklanEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        IklanEntry = form.save(commit=False)
        IklanEntry.user = request.user
        IklanEntry.save()
        return redirect('iklan:show_iklan')
    
    context = {'form': form}    
    return render(request, "create_iklan.html", context)

@login_required
def edit_iklan(request, id_rumah):
    iklan = IklanEntry.objects.get(pk = id_rumah)

    form = IklanEntryForm(request.POST or None, instance=iklan)

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

def show_json(request):
    data = IklanEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id_rumah):
    data = IklanEntry.objects.filter(pk=id_rumah)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id_rumah):
    data = IklanEntry.objects.filter(pk=id_rumah)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_iklan_ajax(request):
    rumah = strip_tags(request.POST.get("rumah"))
    id_rumah = strip_tags(request.POST.get("id_rumah"))
    start_date = strip_tags(request.POST.get("start_date"))
    end_date = strip_tags(request.POST.get("end_date"))
    updated_at = strip_tags(request.POST.get("updated_at"))
    banner = strip_tags(request.POST.get("banner"))

    new_iklan = IklanEntry(
        rumah=rumah, id_rumah=id_rumah,
        start_date=start_date,
        end_date=end_date,
        updated_at=updated_at,
        banner=banner,
    )
    new_iklan.save()

    return HttpResponse(b"CREATED", status=201)