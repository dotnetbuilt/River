from django.urls import path
from .views import get_all_posts, create_post, get_post, delete_post, update_post

urlpatterns = [
    path('get-all/', get_all_posts),
    path('create/', create_post),
    path('get/', get_post),
    path('delete/', delete_post),
    path('update/', update_post),
]
