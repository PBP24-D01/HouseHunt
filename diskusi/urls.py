from django.urls import path
from .views import main_page,show_sellers,review,show_comment,show_sellers_by_id,reply,show_reply,edit_comment,delete_comment
from .views import delete_comment,delete_reply,edit_reply
app_name = 'diskusi'
urlpatterns = [
    path('', main_page, name='diskusi'),
    path('show_sellers/', show_sellers, name='show_sellers'),
    path('review/<int:id>', review, name='review_section'),
    path('show_comment/<int:id>', show_comment, name='show_comments'),
    path('show_seller/<int:id>', show_sellers_by_id, name='show_seller'),
    path('reply/<uuid:id>', reply, name='reply'),
    path('show_reply/<uuid:id>', show_reply, name='show_reply'),   
    path('edit/<uuid:id>',edit_comment, name='edit_comment'),
    path('delete/<uuid:id>',delete_comment, name='delete_comment'),
    path('delete_reply/<uuid:id>',delete_reply, name='delete_reply'),
    path('edit_reply/<uuid:id>',edit_reply, name='edit_reply'),
]