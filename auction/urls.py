from django.urls import path
from . import views

app_name = "auction"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<str:auction_id>/", views.detail, name="detail"),
    path("create/", views.create_auction, name="create"),
    path("edit/<str:auction_id>", views.edit_auction, name="edit"),
    path("delete/<str:auction_id>", views.delete_auction, name="delete"),   
    path("bid/<str:auction_id>", views.bid, name="bid"),
    path("get-all/", views.get_all_auctions, name="get_all_auctions"),
    path("get/<str:auction_id>/", views.get_auction_by_id, name="get_auction_by_id"),
    path("bid/api/<str:auction_id>/", views.bid_api, name="bid_api"),
    path("create/api/", views.create_auction_api, name="create_auction_api"),
    path("edit/api/<str:auction_id>/", views.edit_auction_api, name="edit_auction_api"),
    path("delete/api/<str:auction_id>/", views.delete_auction_api, name="delete_auction_api"),
    path("available-houses/", views.get_available_houses, name="available_houses"),
]
