from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', post_list , name='post_list'),
    path('details/<int:pk>/', post_details , name='post_details'),
    path('new/', new_post , name='new_post'),
    path('<int:pk>/edit/', post_edit , name='post_edit')
]
