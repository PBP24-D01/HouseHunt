from django.shortcuts import render, redirect, get_object_or_404
from wishlist.models import Wishlist
from wishlist.forms import WishlistForm
from rumah.models import House
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.serializers import serialize

# Create your views here.

@login_required(login_url='/login')
def add_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)

    if request.method == 'POST':
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, rumah=rumah)
        if created:
            # Successfully added to wishlist
            return JsonResponse({'status': 'added', 'message': 'Berhasil menambahkan wishlist rumah'}, status=200)
        else:
            # Already exists, remove it
            wishlist.delete()
            return JsonResponse({'status': 'removed', 'message': 'Rumah dihapus dari wishlist'}, status=200)

    return redirect('wishlistpage')

@login_required(login_url='/login')
def delete_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)
    wishlist = Wishlist.objects.filter(user=request.user, rumah=rumah)
    
    if wishlist.exists():
        wishlist.delete()
        message = "Wishlist rumah berhasil dihapus"
    else:
        message = "Rumah tidak ditemukan di wishlist"
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Respond with the status to update the icon on the frontend
        return JsonResponse({'status': 'removed', 'message': message}, status=200)

    return redirect('wishlistpage')

@login_required(login_url='/login')
def edit_wishlist(request, id_rumah):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, rumah__id=id_rumah)
    
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return redirect('wishlistpage')
    else:
        form = WishlistForm(instance=wishlist_item)

    # Get the related house details to pass to the template
    house = wishlist_item.rumah  # This retrieves the House object

    return render(request, 'edit_wishlist.html', {
        'form': form,
        'wishlist_item': wishlist_item,
        'house': house,  # Pass the House object to the template
    })

@login_required(login_url='/login')
def show_wishlist(request):
    # Restrict access to only buyers
    if not request.user.is_buyer:
        return HttpResponseForbidden("Hanya pembeli yang bisa mengakses.")
    
    # Fetch wishlist items for the authenticated user
    wishlists = Wishlist.objects.filter(user=request.user)

    # Get the priority filter from query parameters
    prioritas_filter = request.GET.get('prioritas')
    
    # Filter based on priority if provided
    if prioritas_filter in ['high', 'medium', 'low']:
        wishlists = wishlists.filter(priority=prioritas_filter)

    context = {
        'wishlists': wishlists,
        'prioritas_filter': prioritas_filter,  # To retain the filter in the template
    }
    
    return render(request, 'wishlistpage.html', context)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Wishlist

@login_required(login_url='/login')
def wishlist_json(request):
    # Restrict access to buyers only
    if not request.user.is_buyer:
        return JsonResponse({'error': 'Hanya pembeli yang bisa mengakses.'}, status=403)

    # Fetch wishlist items for the authenticated user
    wishlists = Wishlist.objects.filter(user=request.user)
    
    # Get the priority filter from query parameters (if provided)
    prioritas_filter = request.GET.get('prioritas')
    
    # Filter based on priority if the value is valid
    if prioritas_filter in ['high', 'medium', 'low']:
        wishlists = wishlists.filter(priority=prioritas_filter)

    # Prepare the data for JSON response
    wishlist_data = [
        {
            'id': wishlist.id,
            'rumah_id': wishlist.rumah.id,
            'judul': wishlist.rumah.judul,
            'deskripsi': wishlist.rumah.deskripsi,
            'harga': wishlist.rumah.harga,
            'lokasi': wishlist.rumah.lokasi,
            'gambar': wishlist.rumah.gambar.url if wishlist.rumah.gambar else None,
            'kamar_tidur': wishlist.rumah.kamar_tidur,
            'kamar_mandi': wishlist.rumah.kamar_mandi,
            'prioritas': wishlist.priority,
        }
        for wishlist in wishlists
    ]

    # Return the data in a JSON format
    return JsonResponse({'wishlists': wishlist_data}, status=200)
