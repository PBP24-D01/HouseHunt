from django.urls import path
from iklan.views import show_iklan, create_iklan, edit_iklan, delete_iklan, show_xml , show_xml_by_id, add_iklan_ajax, iklan_json, create_iklan_flutter,edit_iklan_flutter,delete_iklan_flutter
from django.conf import settings
from django.conf.urls.static import static

app_name = 'iklan'

urlpatterns = [
    path('', show_iklan, name='show_iklan'),
    path('create_iklan', create_iklan, name='create_iklan'),
    path('edit_iklan/<int:id_rumah>', edit_iklan, name='edit_iklan'),
    path('delete/<int:id_rumah>', delete_iklan, name='delete_iklan'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<str:id_rumah>/', show_xml_by_id, name='show_xml_by_id'),
    path('create_iklan_ajax', add_iklan_ajax, name='add_iklan_ajax'),
    path('json/', iklan_json, name='iklan_json'),
    path('create/', create_iklan_flutter, name='create_iklan_flutter'),
    path('edit/<int:id_rumah>/', edit_iklan_flutter, name='edit_iklan_flutter'),
    path('delete/<int:id_rumah>/', delete_iklan_flutter, name='delete_iklan_flutter'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
