from django.urls import path
from . import views

urlpatterns = [
    path('', views.linear_regression, name='linear_regression'),
    path('linear_regression_play', views.linear_regression_play, name='linear_regression_play'),
]