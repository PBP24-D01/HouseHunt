from django.shortcuts import render, redirect
from .forms import AvailabilityForm, AppointmentForm
from .models import Availability, Appointment
from rumah.models import House

def create_availability(request):
    seller = request.user.seller  # Assume the seller is the logged-in user
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, seller=seller)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.seller = seller  # Set the seller before saving
            availability.save()
            return redirect('availability_list')  # Redirect to availability list after saving
    else:
        form = AvailabilityForm(seller=seller)

    return render(request, 'availability_form.html', {'form': form})

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.buyer = request.user.buyer  # Assume the buyer is the logged-in user
            appointment.seller = appointment.availability.seller  # Seller is tied to the availability
            appointment.save()
            return redirect('appointment_list')  # Redirect after saving
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})


def availability_list(request):
    seller = request.user.seller
    availabilities = Availability.objects.filter(seller=seller)
    return render(request, 'availability_list.html', {'availabilities': availabilities})


def appointment_list(request):
    buyer = request.user.buyer 
    appointments = Appointment.objects.filter(buyer=buyer)
    return render(request, 'appointment_list.html', {'appointments': appointments})
