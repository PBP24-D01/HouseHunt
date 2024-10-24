from django.urls import path
# from iklan.views import create_iklan
from django.conf import settings
from django.conf.urls.static import static

app_name = 'iklan'

urlpatterns = [
    # path('', create_iklan, name='create_iklan'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
