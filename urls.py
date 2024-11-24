# wardrobe/urls.py

from django.urls import path
from . import views

app_name = 'wardrobe'

urlpatterns = [
    path('', views.wardrobe, name='wardrobe'),
    path('upload/', views.upload_image, name='upload'),
    path('suggest/', views.suggest_outfit, name='suggest_outfit'),
]
