from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/buyer/', views.RegisterBuyer.as_view(), name='buyer_signup'),
    path('register/seller/', views.RegisterSeller.as_view(), name='seller_signup'),
    path("login/", views.login_user, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]