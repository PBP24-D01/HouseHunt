from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<str:auction_id>/", views.detail, name="detail"),
    path("create/", views.create_auction, name="create"),
    path("edit/<str:auction_id>", views.create_auction, name="create"),
    path("delete-ajax", views.delete_auction, name="delete"),   
    path("bid-ajax", views.bid, name="bid"),
]
