from django.shortcuts import render, redirect
from .models import House
from .forms import HouseForm


# Create your views here.

def jual_rumah(request):
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            rumah = form.save(commit=False)
            rumah.seller = request.user # Assign penjual

            rumah.save()
            return redirect('') # Somewhere
    else:
        form = HouseForm()
    return render(request, 'rumah/jual_rumah.html', {'form': form}) 

def update_rumah(request, pk):
    rumah = House.objects.get(pk=pk, seller = request.user)
    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=rumah)
        if form.is_valid():
            form.save()
            return redirect('') # Somewhere
        else:
            form = HouseForm(instance=rumah)
    return render(request, 'rumah/update_rumah.html', {'form': form})

def delete_rumah(request,pk):
    rumah = House.objects.get(pk=pk, seller = request.user)
    rumah.delete()
    return redirect('') # Somewhere