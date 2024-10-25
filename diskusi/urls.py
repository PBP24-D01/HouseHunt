from django.urls import path
from .views import main_page
app_name = 'diskusi'
urlpatterns = [
    path('diskusi/', main_page, name='diskusi'),
]