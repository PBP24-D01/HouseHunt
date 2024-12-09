from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'houses'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('house/<int:house_id>/', views.house_detail, name='house_detail'),
    path('house/create/', views.house_create, name='house_create'),
    path('house/edit/<int:house_id>/', views.house_edit, name='house_edit'),
    path('house/delete/<int:house_id>/', views.house_delete, name='house_delete'),
    path('order/<int:house_id>/', views.order_page, name='order_page'),
    path('invoice/<int:house_id>/', views.generate_invoice, name='generate_invoice'),
    path('api/filter-options/', views.get_filter_options, name = 'get_filter_options'),
    path('api/houses/', views.get_houses, name = 'get_houses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
