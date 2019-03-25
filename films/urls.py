# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('film/create/', views.film_create, name='film-create'),
    path('film/<int:id>/update/', views.film_update, name='film-update'),
    path('film/<int:id>/delete/', views.film_delete, name='film-delete'),
    path('allfilms/', views.all_films, name='all-films'),
    path('myfilms/', views.my_films, name='my-films'),

    path('film/<int:film_id>/comments/', views.film_comments, name='film-comments'),
    path('comment/<int:id>/update/', views.comment_update, name='comment-update'),
    path('comment/<int:id>/delete/', views.comment_delete, name='comment-delete'),
    path('allcomments/', views.all_comments, name='all-comments'),
    path('mycomments/', views.my_comments, name='my-comments'),
]