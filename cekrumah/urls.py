from django.urls import path
from cekrumah.views import update_appointment_api, fetch_availabilities_by_house, get_buyer_houses, fetch_appointments_buyer, update_appointment_status, update_availability_api, delete_availability_api, get_seller_houses, fetch_availabilities, fetch_appointments, delete_appointment_api, get_availability_api, create_appointment_api, create_availability, create_appointment, availability_list, appointment_list, create_availability_api, delete_appointment, delete_availability, update_appointment, update_availability, get_availability

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
    path('api/create_availability/', create_availability_api, name='create-availability-api'),
    path('api/create_appointment/', create_appointment_api, name='create-appointment-api'),
    path('api/availability/list/', get_availability_api, name='get-availability-api'),
    path('api/delete_appointment/<int:appointment_id>/', delete_appointment_api, name='delete-appointment-api'),
    path('api/appointments/', fetch_appointments, name='fetch_appointments'),
    path('api/availabilities/', fetch_availabilities, name='fetch_availabilities'),
    path('api/seller_houses/', get_seller_houses, name="get_seller_houses"),
    path('api/availability/delete/', delete_availability_api, name="delete_availability_api"),
    path('api/availability/update/', update_availability_api, name='update_availability_api'),
    path('api/update_appointment_status/', update_appointment_status, name='update_appointment_status'),
    path('api/appointments/buyer/', fetch_appointments_buyer, name='fetch_appointments_buyer'),
    path('api/buyer_houses/', get_buyer_houses, name="get_buyer_houses"),
    path('api/availabilities/<int:houseId>/', fetch_availabilities_by_house, name='fetch_availabilities_by_house'),
    path('api/update_appointment/<int:appointmentId>/', update_appointment_api, name="update_appointment_api")
]