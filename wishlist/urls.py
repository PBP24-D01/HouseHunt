from django.urls import path
from wishlist.views import add_wishlist, delete_wishlist, show_wishlist, edit_wishlist
from wishlist.views import wishlist_json, delete_wishlist_flutter, edit_wishlist_flutter

urlpatterns = [
    path('wishlist/', show_wishlist, name='wishlistpage'),
    path('wishlist/add/<int:id_rumah>/', add_wishlist, name='add_wishlist'),
    path('wishlist/delete/<int:id_rumah>/', delete_wishlist, name='delete_wishlist'),
    path('wishlist/edit/<int:id_rumah>/', edit_wishlist, name='edit_wishlist'),
    path('wishlist/json/', wishlist_json, name='wishlist_json'),
    path('wishlist/delete-flutter/<int:id_rumah>/', delete_wishlist_flutter, name='delete_wishlist_flutter'),
    path('wishlist/edit-flutter/<int:id_rumah>/', edit_wishlist_flutter, name='edit_wishlist_flutter'),
]