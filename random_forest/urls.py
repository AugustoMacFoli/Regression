from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_forest, name='random_forest'),
    path('random_forest', views.random_forest_play, name='random_forest_play'),
]