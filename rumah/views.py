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
from django.conf import settings

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


def get_filter_options(request):
    filter_options = {
        'locations': [choice[0] for choice in HouseFilterForm.LOCATION_CHOICES if choice[0]],
        'price_ranges': [choice[0] for choice in HouseFilterForm.PRICE_CHOICES if choice[0]],
        'bedrooms': [choice[0] for choice in HouseFilterForm.BEDROOM_CHOICES if choice[0]],
        'bathrooms': [choice[0] for choice in HouseFilterForm.BATHROOM_CHOICES if choice[0]],
    }
    return JsonResponse(filter_options)

def get_houses(request):
    houses = House.objects.all()
    
    # filters
    lokasi = request.GET.get('lokasi')
    if lokasi:
        houses = houses.filter(lokasi=lokasi)
    
    price_range = request.GET.get('price_range')
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        houses = houses.filter(harga__gte=min_price, harga__lte=max_price)
    
    kamar_tidur = request.GET.get('kamar_tidur')
    if kamar_tidur:
        if kamar_tidur == '4+':
            houses = houses.filter(kamar_tidur__gte=4)
        else:
            houses = houses.filter(kamar_tidur=int(kamar_tidur))
    
    kamar_mandi = request.GET.get('kamar_mandi')
    if kamar_mandi:
        if kamar_mandi == '3+':
            houses = houses.filter(kamar_mandi__gte=3)
        else:
            houses = houses.filter(kamar_mandi=int(kamar_mandi))
    
    is_available = request.GET.get('is_available')
    if is_available:
        houses = houses.filter(is_available=True)
    
    house_list = []
    for house in houses:
        house_data = {
            'id': house.id,
            'judul': house.judul,
            'deskripsi': house.deskripsi,
            'lokasi': house.lokasi,
            'harga': house.harga,
            'kamar_tidur': house.kamar_tidur,
            'kamar_mandi': house.kamar_mandi,
            'is_available': house.is_available,
            'gambar': request.build_absolute_uri(house.gambar.url) if house.gambar else None,
        }
        house_list.append(house_data)
    
    return JsonResponse(house_list, safe=False)

@csrf_exempt
def api_house_create(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)

        if form.is_valid():
            house = form.save(commit=False)
            house.save()
            return JsonResponse({'message': 'House created successfully!', 'id': house.id}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def api_order_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if not house.is_available:
        return JsonResponse({'error': 'House is not available'}, status=400)
    if request.user.is_authenticated:
        if hasattr(request.user, 'buyer'):
            buyer = request.user.buyer
            house_data = {
                'judul': house.judul,
                'harga': house.harga,
                'lokasi': house.lokasi,
                'deskripsi': house.deskripsi,
                'kamar_tidur': house.kamar_tidur,
                'kamar_mandi': house.kamar_mandi,
                'penjual': house.seller.user.username,
                'kontak_penjual': house.seller.user.email,
            }
            return JsonResponse({'house': house_data})
        else:
            return JsonResponse({'error': 'User is not a buyer'}, status=400)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    
@csrf_exempt
def api_generate_invoice(request, house_id):
    house = get_object_or_404(House, id=house_id)
    if not house.is_available:
        return JsonResponse({'error': 'House is not available'}, status=400)
    if request.user.is_authenticated:
        if hasattr(request.user, 'buyer'):
            buyer = request.user.buyer
            house.is_available = False
            house.save()
            house_data = {
                'id': house.id,
                'judul': house.judul,
                'harga': house.harga,
                'lokasi': house.lokasi,
                'deskripsi': house.deskripsi,
                'kamar_tidur': house.kamar_mandi,
                'kamar_mandi': house.kamar_tidur,
                'seller': {
                    'username': house.seller.user.username,
                    'email': house.seller.user.email,
                }
            }
            buyer_data = {
                'username': buyer.user.username,
                'email': buyer.user.email,
            }
            return JsonResponse({'house': house_data, 'buyer': buyer_data, 'total_price': house.harga}) 
        else:
            return JsonResponse({'error': 'User is not a buyer'}, status=400)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)