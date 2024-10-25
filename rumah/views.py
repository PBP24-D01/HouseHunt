from django.shortcuts import render, redirect, get_object_or_404
from .models import House
from .forms import HouseFilterForm

# Create your views here.

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