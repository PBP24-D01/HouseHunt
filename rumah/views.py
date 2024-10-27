from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import House
from wishlist.models import Wishlist
from .forms import HouseForm, HouseFilterForm
from HouseHuntAuth.models import Seller, Buyer
from iklan.models import IklanEntry

def landing_page(request):
    form = HouseFilterForm(request.GET or {'is_available': True})
    houses = House.objects.all()
    ads = IklanEntry.objects.all()
    
    # Initialize user_wishlist to an empty list
    user_wishlist = []


    if request.user.is_authenticated:
        # Query the Wishlist directly using the CustomUser instance
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('rumah', flat=True)

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

        # is available
        is_available = form.cleaned_data.get('is_available')
        if is_available is not None:
            houses = houses.filter(is_available=is_available)

    context = {
        'houses': houses,
        'form': form,
        'user_wishlist': user_wishlist,  # List of house IDs
        'ads' : ads
    }
    return render(request, 'landing_page.html', context)

def house_detail(request, house_id):
    house = get_object_or_404(House, id=house_id)
    return render(request, 'house_detail.html', {'house': house})

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


@login_required
def order_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if not house.is_available:
        return redirect('houses:house_detail', house_id=house.id)
    if hasattr(request.user, 'buyer'):
        buyer = request.user.buyer
        return render(request, 'order_page.html', {'house': house, 'buyer': buyer})
    else:
        return redirect('houses:house_detail', house_id=house.id)

@login_required
def generate_invoice(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if not house.is_available:
        return redirect('houses:house_detail', house_id=house.id)
    if hasattr(request.user, 'buyer'):
        buyer = request.user.buyer
        house.is_available = False
        house.save()
        return render(request, 'invoice.html', {'house': house, 'buyer': buyer})
    else:
        return redirect('houses:house_detail', house_id=house.id)