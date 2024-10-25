from django.urls import path
from wishlist.views import add_wishlist, delete_wishlist, show_wishlist

urlpatterns = [
    path('', show_wishlist, name='wishlistpage'),
    path('add/<uuid:id_rumah>/', add_wishlist, name='add_wishlist'),
    path('remove/<uuid:id_rumah>/', delete_wishlist, name='delete_wishlist'),
]