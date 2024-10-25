from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'houses'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('house/<int:house_id>/', views.house_detail, name='house_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)