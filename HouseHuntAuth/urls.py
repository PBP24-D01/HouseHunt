from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "HouseHuntAuth"

urlpatterns = [
    path("register/buyer/", views.RegisterBuyer.as_view(), name="buyer_signup"),
    path("register/seller/", views.RegisterSeller.as_view(), name="seller_signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("login/flutter/", views.login, name="login_flutter"),
    path("register/buyer/flutter/", views.register_buyer, name="buyer_signup_flutter"),
    path("register/seller/flutter/", views.register_seller, name="seller_signup_flutter"),
    path("logout/flutter/", views.logout, name="logout_flutter"),
]
