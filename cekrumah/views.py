from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from HouseHuntAuth.models import Seller
from .forms import AvailabilityForm, AppointmentForm, AppointmentStatusForm
from .models import Availability, Appointment
from rumah.models import House
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="/login")
def create_availability(request):
    if not hasattr(request.user, 'seller'):
        return HttpResponse("You are not a seller", status=403)
    
    seller = request.user.seller  # Assume the seller is the logged-in user
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, seller=seller)
        if form.is_valid():
            try:
                availability = form.save(commit=False)
                availability.seller = request.user.seller  # Set the seller before saving
                availability.save()
                messages.success(request, "Availability added successfully")
                return redirect('cekrumah:availability_list')  # Redirect to availability list after saving
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
    else:
        form = AvailabilityForm(seller=seller)

    return render(request, 'availability_form.html', {'form': form})

@login_required(login_url="/login")
def create_appointment(request):
    if not hasattr(request.user, 'buyer'):
        return HttpResponse("You are not a buyer", status=403)
    
    # Initialize the form outside of the POST check
    form = AppointmentForm()

    if request.method == 'POST':
        house_id = request.POST.get('house')
        availability_id = request.POST.get('availability')  # Assuming you need to fetch this as well
        form = AppointmentForm(request.POST, house_id=house_id)

        # Check if the required fields are present
        if not house_id or not availability_id:
            messages.error(request, "Please select a house and an available slot.")
        elif form.is_valid():
            appointment = form.save(commit=False)
            appointment.buyer = request.user.buyer  # Assuming buyer is logged-in user
            appointment.seller = appointment.availability.seller  # Seller tied to the availability
            appointment.save()
            messages.success(request, "Appointment created successfully!")  # Success message
            return redirect('cekrumah:appointment_list')  # Redirect after saving

    # Fetch all available houses for the buyer
    houses = House.objects.filter(is_available=True)  # Adjust based on your model attributes
    return render(request, 'appointment_form.html', {'form': form, 'houses': houses})

# ini buat mengambil data availabilities secara AJAX
@login_required(login_url="/login")
def get_availability(request):
    if request.method == 'GET':
        house_id = request.GET.get('house_id')
        if house_id:
            availabilities = Availability.objects.filter(house_id=house_id, is_available=True)
            data = [{'id': availability.id, 
                     'date': availability.available_date, 
                     'start_time': availability.start_time.strftime('%H:%M'),  
                    'end_time': availability.end_time.strftime('%H:%M')
                    } for availability in availabilities]
            return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url="/login")
def availability_list(request):
    if not hasattr(request.user, 'seller'):
        return HttpResponse("You are not a seller", status=403)
    seller = request.user.seller
    availabilities = Availability.objects.filter(seller=seller)
    appointments = Appointment.objects.filter(seller=seller)
    # Process the appointment status update form if submitted
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id, seller=seller)
        form = AppointmentStatusForm(request.POST, instance=appointment)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment status updated successfully.")
            return redirect('cekrumah:availability_list')
        else:
            messages.error(request, "Failed to update appointment status.")
    else:
        form = AppointmentStatusForm()

    return render(request, 'availability_list.html', {
        'availabilities': availabilities,
        'appointments': appointments,
        'form': form,
    })

@login_required(login_url="/login")
def appointment_list(request):
    if not hasattr(request.user, 'buyer'):
        return HttpResponse("You are not a buyer", status=403)
    buyer = request.user.buyer 
    appointments = Appointment.objects.filter(buyer=buyer)
    return render(request, 'appointment_list.html', {'appointments': appointments})


# Delete Appointment
@login_required(login_url="/login")
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect('cekrumah:appointment_list')


# Delete Availability
@login_required(login_url="/login")
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)
    availability.delete()
    messages.success(request, "Availability deleted successfully.")
    return redirect('cekrumah:availability_list')



# Update Appointment
@login_required(login_url="/login")
def update_appointment(request, appointment_id):
    if not hasattr(request.user, 'buyer'):
        return HttpResponse("You are not a buyer", status=403)
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    houses = House.objects.filter(is_available=True, id=appointment.availability.house.id)  # Fetch all available houses
    
    if request.method == 'POST':
        house_id = request.POST.get('house')
        availability_id = request.POST.get('availability')  # Assuming you need to fetch this as well
        form = AppointmentForm(request.POST, instance=appointment, house_id=appointment.availability.house.id)

        # Check if the required fields are present
        if not house_id or not availability_id:
            messages.error(request, "Please select a house and an available slot.")
        elif form.is_valid():
            appointment = form.save(commit=False)
            appointment.buyer = request.user.buyer  # Maintain the buyer relationship
            appointment.seller = appointment.availability.seller  # Seller tied to the availability
            appointment.save()
            messages.success(request, "Appointment updated successfully!")  # Success message
            return redirect('cekrumah:appointment_list')  # Redirect to list of appointments
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointment_form.html', {'form': form, 'houses': houses})



# Update Availability
@login_required(login_url="/login")
def update_availability(request, availability_id):
    if not hasattr(request.user, 'seller'):
        return HttpResponse("You are not a seller", status=403)
    
    availability = get_object_or_404(Availability, id=availability_id)
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            messages.success(request, "Availability updated successfully!")
            return redirect('cekrumah:availability_list')  # Redirect to list of availabilities
    else:
        form = AvailabilityForm(instance=availability)

    return render(request, 'availability_form.html', {'form': form})
