from django.urls import path
from cekrumah.views import create_availability, create_appointment, availability_list, appointment_list

app_name = 'cekrumah'

urlpatterns = [
    path('appointment/create/', create_appointment, name='create_appointment'),
    path('availability/create/', create_availability, name='create_availability'),
    path('availability/list/', availability_list, name='availability_list'),
    path('appointment/list/', appointment_list, name='appointment_list'),
]