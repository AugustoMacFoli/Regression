from django.urls import path
from . import views

urlpatterns = [
    path('', views.svr, name='svr'),
    path('svr_play', views.svr_play, name='svr_play'),
]