from django.urls import path
from . import views

app_name = "auction"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<str:auction_id>/", views.detail, name="detail"),
    path("create/", views.create_auction, name="create"),
    path("edit/<str:auction_id>", views.edit_auction, name="edit"),
    path("delete/<str:auction_id>", views.delete_auction, name="delete"),   
    path("bid-ajax", views.bid, name="bid"),
    path("get-all", views.get_all_auctions, name="get_all_auctions"),
    path("get/<str:auction_id>", views.get_auction_by_id, name="get_auction_by_id"),
]
