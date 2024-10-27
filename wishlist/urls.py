from django.urls import path
from wishlist.views import add_wishlist, delete_wishlist, show_wishlist, edit_wishlist

urlpatterns = [
    path('wishlist/', show_wishlist, name='wishlistpage'),
    path('wishlist/add/<int:id_rumah>/', add_wishlist, name='add_wishlist'),
    path('wishlist/delete/<int:id_rumah>/', delete_wishlist, name='delete_wishlist'),
    path('wishlist/edit/<int:id_rumah>/', edit_wishlist, name='edit_wishlist'),
]