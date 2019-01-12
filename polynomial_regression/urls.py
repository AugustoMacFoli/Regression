from django.urls import path
from . import views

urlpatterns = [
    path('', views.polynomial_regression, name='polynomial_regression'),
    path('polynomial_regression_play', views.polynomial_regression_play, name='polynomial_regression_play'),
]