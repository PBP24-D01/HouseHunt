from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:auction_id>/", views.detail, name="detail"),
    path("<int:auction_id>/bid/", views.bid, name="bid"),
    path("create/", views.create, name="create"),
]
