from django.urls import path
from cekrumah.views import fetch_availabilities, fetch_appointments, delete_appointment_api, update_availability_api, get_availability_api, create_appointment_api, create_availability, create_appointment, availability_list, appointment_list, create_availability_api, delete_appointment, delete_availability, update_appointment, update_availability, get_availability

app_name = 'cekrumah'

urlpatterns = [
    path('appointment/create/', create_appointment, name='create_appointment'),
    path('availability/create/', create_availability, name='create_availability'),
    path('availability/list/', availability_list, name='availability_list'),
    path('appointment/list/', appointment_list, name='appointment_list'),
    path('appointment/<int:appointment_id>/delete/', delete_appointment, name='delete_appointment'),
    path('availability/<int:availability_id>/delete/', delete_availability, name='delete_availability'),
    path('appointment/<int:appointment_id>/update/', update_appointment, name='update_appointment'),
    path('availability/<int:availability_id>/update/', update_availability, name='update_availability'),
    path('get-availability/', get_availability, name='get_availability'),
    path('api/availability/', create_availability_api, name='create-availability-api'),
    path('api/appointment/', create_appointment_api, name='create-appointment-api'),
    path('api/availability/list/', get_availability_api, name='get-availability-api'),
    path('api/availability/<int:availability_id>/', update_availability_api, name='update-availability-api'),
    path('api/appointment/<int:appointment_id>/', delete_appointment_api, name='delete-appointment-api'),
    path('api/appointments/', fetch_appointments, name='fetch_appointments'),
    path('api/availabilities/', fetch_availabilities, name='fetch_availabilities'),
]