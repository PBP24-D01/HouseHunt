from django.urls import path
from cekrumah.views import create_availability, create_appointment, availability_list, appointment_list, delete_appointment, delete_availability, update_appointment, update_availability, get_availability

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
]