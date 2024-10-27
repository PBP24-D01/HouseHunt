from django.urls import path
from .views import main_page,show_sellers,review,show_comment,show_sellers_by_id
app_name = 'diskusi'
urlpatterns = [
    path('diskusi/', main_page, name='diskusi'),
    path('diskusi/show_sellers/', show_sellers, name='show_sellers'),
    path('diskusi/review/<int:id>', review, name='review_section'),
    path('diskusi/show_comment/<int:id>', show_comment, name='show_comments'),
    path('diskusi/show_seller/<int:id>', show_sellers_by_id, name='show_seller'),
]