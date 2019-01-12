from django.urls import path
from . import views

urlpatterns = [
    path('', views.multiple_linear_regression, name='multiple_linear_regression'),
    path('multiple_linear_regression_play', views.multiple_linear_regression_play, name='multiple_linear_regression_play'),
]