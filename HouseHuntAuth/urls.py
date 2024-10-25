from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/buyer/', views.RegisterBuyer.as_view(), name='buyer_signup'),
    path('signup/seller/', views.RegisterSeller.as_view(), name='seller_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='marketplace/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]