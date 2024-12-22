from datetime import datetime

from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from HouseHuntAuth.models import Seller
from .forms import AvailabilityForm, AppointmentForm, AppointmentStatusForm
from .models import Availability, Appointment
from rumah.models import House
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import json


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


@csrf_exempt
def create_appointment_api(request):
    if not hasattr(request.user, 'buyer'):
        return JsonResponse({"error": "You are not a buyer"}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            get_availability = Availability.objects.get(id=data['availability_id'])

            appointment = Appointment(
                buyer=request.user.buyer,
                seller=get_availability.seller,
                availability = get_availability,
                notes_to_seller=data['notes'],
            )
            appointment.save()
            return JsonResponse({"success": True, "message": "Appointment has been made","appointment_id": appointment.id}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": e.message_dict}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_availability_api(request):
    house_id = request.GET.get('house_id')
    if house_id:
        availabilities = Availability.objects.filter(house_id=house_id, is_available=True)
        data = [
            {
                'id': availability.id,
                'date': availability.available_date,
                'start_time': availability.start_time.strftime('%H:%M'),
                'end_time': availability.end_time.strftime('%H:%M'),
            }
            for availability in availabilities
        ]
        return JsonResponse(data, safe=False)

    return JsonResponse({"error": "House ID is required"}, status=400)


@csrf_exempt
def delete_appointment_api(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, buyer=request.user.buyer)

    if request.method == 'POST':
        appointment.delete()
        return JsonResponse({"message": "Appointment deleted successfully", 'success': True}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def fetch_appointments(request):
    if request.method == 'GET':
        user = request.user
        print(user)
        try:
            # Retrieve appointments for the logged-in user (as a buyer)
            appointments = Appointment.objects.filter(seller= user.seller)
            # Serialize appointment data
            appointments_data = []
            for appointment in appointments:
                appointments_data.append({
                    'id': appointment.id,
                    'house': {
                        'id': appointment.availability.house.id,
                        'name': str(appointment.availability.house)
                    },
                    'buyer': {
                        'username': appointment.buyer.user.username,
                        'email': appointment.buyer.user.email
                    },
                    'date': appointment.availability.available_date.strftime('%Y-%m-%d'),
                    'start_time': appointment.availability.start_time.strftime('%H:%M:%S'),
                    'end_time': appointment.availability.end_time.strftime('%H:%M:%S'),
                    'status': appointment.get_status_display(),
                    'notes_to_seller': appointment.notes_to_seller,
                })
            print(appointments_data)
            return JsonResponse({'success': True, 'appointments': appointments_data}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error fetching appointments', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@login_required
def fetch_appointments_buyer(request):
    if request.method == 'GET':
        user = request.user
        print(user)
        try:
            # Retrieve appointments for the logged-in user (as a buyer)
            appointments = Appointment.objects.filter(buyer = user.buyer)
            print(appointments)
            # Serialize appointment data
            appointments_data = []
            for appointment in appointments:
                appointments_data.append({
                    'id': appointment.id,
                    'house': {
                        'id': appointment.availability.house.id,
                        'name': str(appointment.availability.house)
                    },
                    'availability': {
                        'id': appointment.availability.id
                    },
                    'seller': {
                        'username': appointment.availability.seller.user.username,
                    },
                    'date': appointment.availability.available_date.strftime('%Y-%m-%d'),
                    'start_time': appointment.availability.start_time.strftime('%H:%M:%S'),
                    'end_time': appointment.availability.end_time.strftime('%H:%M:%S'),
                    'status': appointment.get_status_display(),
                    'notes_to_seller': appointment.notes_to_seller,
                })
            print(appointments_data)
            return JsonResponse({'success': True, 'appointments': appointments_data}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error fetching appointments', 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def fetch_availabilities(request):
    if request.method == 'GET': 
        user = request.user
        try:
            availabilities = Availability.objects.filter(
                house__seller__user=user
            ).select_related('house')

            availabilities_data = [
                {
                    'id': availability.id,
                    'house': {
                        'id': availability.house.id,
                        'name': str(availability.house),
                    },
                    'available_date': availability.available_date.strftime('%Y-%m-%d'),
                    'start_time': availability.start_time.strftime('%H:%M:%S'),
                    'end_time': availability.end_time.strftime('%H:%M:%S'),
                    'is_available': availability.is_available,
                }
                for availability in availabilities
            ]
            return JsonResponse({'success': True, 'availabilities': availabilities_data}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    
@csrf_exempt
def fetch_availabilities_by_house(request, houseId):
    if request.method == 'GET': 
        user = request.user
        try:
            availabilities = Availability.objects.filter(
                house__id = houseId
            )

            availabilities_data = [
                {
                    'id': availability.id,
                    'date': availability.available_date,
                    'start_time': availability.start_time,
                    'end_time': availability.end_time
                }
                for availability in availabilities
            ]
            return JsonResponse({'success': True, 'availabilities': availabilities_data}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    

def get_seller_houses(request):
    if request.method == 'GET':
        user = request.user
        print(f"User: {user}, Authenticated: {user.is_authenticated}")
        print(user.seller)
        try:
            houses = House.objects.filter(seller = user.seller)
            # print(houses)
            houses_data = [
                {
                    'id': house.id,
                    'judul': house.judul
                } for house in houses
            ]
            return JsonResponse({'houses':houses_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

def get_buyer_houses(request):
    if request.method == 'GET':
        user = request.user
        print(f"User: {user}, Authenticated: {user.is_authenticated}")
        try:
            houses = House.objects.all()
            # print(houses)
            houses_data = [
                {
                    'id': house.id,
                    'judul': house.judul
                } for house in houses
            ]
            return JsonResponse({'houses':houses_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def create_availability_api(request):
    if not hasattr(request.user, 'seller'):
        return JsonResponse({"success": False}, status=403)

    seller = request.user.seller
    print("########### CREATE ############")
    print(seller)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            house = House.objects.get(id=data['house_id'], seller=seller)
            print(house)
            # Assuming data['available_date'] is '2024-12-20T00:00:00.000'
            available_date = datetime.strptime(data['available_date'], '%Y-%m-%dT%H:%M:%S.%f').date()
            start_time = data['start_time']  # Example: '5:46 PM'
            end_time = data['end_time']    # Example: '6:30 PM'

            # Convert from 12-hour format to 24-hour format
            start_time_24hr = datetime.strptime(start_time, '%I:%M %p').time()  # %I is 12-hour, %p is AM/PM
            end_time_24hr = datetime.strptime(end_time, '%I:%M %p').time()

            print(available_date)
            availability = Availability(
                seller= seller,
                house = house,
                available_date=available_date,
                start_time=start_time_24hr,
                end_time=end_time_24hr,
            )
            print(availability)
            availability.save()
            return JsonResponse({"success": True, "availability_id": availability.id}, status=201)
        except ValidationError as e:
            print(e)
        except KeyError as e:
            print(e)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_availability_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        availability_id = data['id']
       
        availability = Availability.objects.filter(id=availability_id)

        availability.delete()
        return JsonResponse({'success':True}, status=200)
    
    return JsonResponse({}, status=405)

@csrf_exempt
def update_availability_api(request):
    if not hasattr(request.user, 'seller'):
        return JsonResponse({"success": False}, status=403)
    
    seller = request.user.seller
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data['id'])
            old = Availability.objects.get(id=data['id'])
            # print(data)
            print(old)
            house = House.objects.get(id=data['house_id'], seller=seller)
            # Assuming data['available_date'] is '2024-12-20T00:00:00.000'
            available_date = datetime.strptime(data['available_date'], '%Y-%m-%dT%H:%M:%S.%f').date()
            start_time = data['start_time']  # Example: '5:46 PM'
            end_time = data['end_time']    # Example: '6:30 PM'

            # Convert from 12-hour format to 24-hour format
            if(start_time.endswith("M")):
                start_time = datetime.strptime(start_time, '%I:%M %p').time()  # %I is 12-hour, %p is AM/PM
            
            
            if(end_time.endswith("M")):
                end_time = datetime.strptime(end_time, '%I:%M %p').time()
            
            
            old.house = house
            old.available_date=available_date
            old.start_time=start_time
            old.end_time=end_time
  
            
            old.save()
            return JsonResponse({"success": True, "availability_id": old.id}, status=201)
        except ValidationError as e:
            print(e)
        except KeyError as e:
            print(e)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_appointment_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            appointment_id = data.get('id')
            new_status = data.get('status')

            # Validasi input
            if not appointment_id or not new_status:
                return JsonResponse({"success": False, "message": "Invalid data"}, status=400)

            # Update status appointment
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = new_status
            appointment.save()

            return JsonResponse({"success": True, "message": "Status updated successfully"})
        except Appointment.DoesNotExist:
            return JsonResponse({"success": False, "message": "Appointment not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def update_appointment_api(request, appointmentId):
    if not hasattr(request.user, 'buyer'):
        return JsonResponse({"error": "You are not a buyer"}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            get_availability = Availability.objects.get(id=data['availability_id'])
            old = Appointment.objects.get(id=appointmentId)

            old.buyer=request.user.buyer
            old.seller=get_availability.seller
            old.availability = get_availability
            old.notes_to_seller=data['notes']
            old.status='Pending'
            
            old.save()
            return JsonResponse({"success": True, "message": "Appointment has been updated","appointment_id": old.id}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": e.message_dict}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field: {e}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
