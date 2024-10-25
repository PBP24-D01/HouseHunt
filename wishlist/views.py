from django.shortcuts import render, redirect, get_object_or_404
from wishlist.models import Wishlist
from wishlist.forms import WishlistForm
from rumah.models import House
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def add_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, rumah=rumah)
    if created:
        message = "Berhasil menambahkan wishlist rumah"
    else:
        message = "Rumah sudah ada pada wishlist"
    return redirect('wishlist_view')

@login_required
def delete_wishlist(request, id_rumah):
    rumah = get_object_or_404(House, id=id_rumah)
    Wishlist.objects.filter(user=request.user, rumah=rumah).delete()
    return redirect('wishlist_view')

@login_required
def edit_wishlist(request, id_rumah):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, id_rumah=id_rumah)
    
    if request.method == 'POST':
        form = WishlistForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return redirect('wishlist_view')
    else:
        form = WishlistForm(instance=wishlist_item)
    
    return render(request, 'wishlist_update.html', {'form': form})