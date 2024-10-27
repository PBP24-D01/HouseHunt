from django.shortcuts import render, redirect, get_object_or_404
from wishlist.models import Wishlist
from wishlist.forms import WishlistForm
from rumah.models import House
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.

@login_required(login_url='/login')
def add_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, rumah=rumah)
    if created:
        message = "Berhasil menambahkan wishlist rumah"
    else:
        message = "Rumah sudah ada pada wishlist"
    return redirect('wishlistpage')

@login_required(login_url='/login')
def delete_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)
    Wishlist.objects.filter(user=request.user, rumah=rumah).delete()
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
    if not request.user.is_buyer:
        return HttpResponseForbidden("Hanya pembeli yang bisa mengakses.")
    
    wishlists = Wishlist.objects.filter(user=request.user)
    
    context = {
        'wishlists': wishlists
    }
    
    return render(request, 'wishlistpage.html', context)
