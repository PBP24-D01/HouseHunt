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
    path('api/houses/create/', views.api_house_create, name='api_house_create'),
    path('api/form-options/', views.get_filter_options, name='form-options'),
    path('api/order/<int:house_id>/', views.api_order_page, name='api_order_page'), 
    path('api/invoice/<int:house_id>/', views.api_generate_invoice, name='api_generate_invoice'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)