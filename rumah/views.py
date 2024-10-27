from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import House
from .forms import HouseForm, HouseFilterForm
from HouseHuntAuth.models import Seller

def landing_page(request):
    form = HouseFilterForm(request.GET)
    houses = House.objects.filter(is_available=True)
    
    if form.is_valid():
        # harga
        price_range = form.cleaned_data.get('price_range')
        if price_range:
            min_price, max_price = map(int, price_range.split('-'))
            houses = houses.filter(harga__gte=min_price, harga__lte=max_price)
            
        # lokasi
        lokasi = form.cleaned_data.get('lokasi')
        if lokasi:
            houses = houses.filter(lokasi__icontains=lokasi)
            
        # kamar tidur
        kamar_tidur = form.cleaned_data.get('kamar_tidur')
        if kamar_tidur: 
            if kamar_tidur == '4+':
                houses = houses.filter(kamar_tidur__gte=4)
            else:
                houses = houses.filter(kamar_tidur=int(kamar_tidur))
                
        # kamar mandi
        kamar_mandi = form.cleaned_data.get('kamar_mandi')
        if kamar_mandi:
            if kamar_mandi == '3+':
                houses = houses.filter(kamar_mandi__gte=3)
            else:
                houses = houses.filter(kamar_mandi=int(kamar_mandi))
    
    context = {
        'houses': houses,
        'form': form,
    }
    return render(request, 'landing_page.html', context)

def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'house_detail.html', {'house': house})


#@csrf_protect
@csrf_exempt
def house_create(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)

        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            return JsonResponse({'error': 'You must be a seller to create a house.'}, status=400)
        
        if form.is_valid():
            house = form.save(commit=False)
            house.seller = seller
            house.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'House created successfully!'}, status=200)
            else:
                return redirect('houses:landing_page')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                return render(request, 'house_form.html', {'form': form, 'errors': form.errors})
    else:
        form = HouseForm()
    return render(request, 'house_form.html', {'form': form})

@login_required
def settings(request):
    return render(request, 'settings.html')

@login_required
def house_edit(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if request.user != house.seller.user:
        return redirect('houses:house_detail', house_id=house.id)
    
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            return redirect('houses:house_detail', house_id=house.id)
    else:
        form = HouseForm(instance=house)
    
    return render(request, 'house_edit.html', {'form': form, 'house': house})

def house_delete(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if request.user != house.seller.user:
        return redirect('houses:house_detail', house_id=house.id)
    
    house.delete()
    return redirect('houses:landing_page')