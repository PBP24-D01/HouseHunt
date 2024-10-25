from django.urls import path
from . import views

app_name = 'houses'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('house/<int:house_id>/', views.house_detail, name='house_detail'),
]