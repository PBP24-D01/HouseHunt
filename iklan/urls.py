from django.urls import path
from iklan.views import show_iklan, create_iklan, edit_iklan, delete_iklan, show_xml, show_json, show_xml_by_id, show_json_by_id, add_iklan_ajax
from django.conf import settings
from django.conf.urls.static import static

app_name = 'iklan'

urlpatterns = [
    path('', show_iklan, name='show_iklan'),
    path('create-item-entry', create_iklan, name='create_iklan'),
    path('edit-item/<uuid:id_rumah>', edit_iklan, name='edit_iklan'),
    path('delete/<uuid:id_rumah>', delete_iklan, name='delete_iklan'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id_rumah>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id_rumah>/', show_json_by_id, name='show_json_by_id'),
    path('create-iklan-ajax', add_iklan_ajax, name='add_iklan_ajax'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
