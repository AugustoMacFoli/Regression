from django.urls import path
from . import views

urlpatterns = [
    path('', views.decision_tree, name='decision_tree'),
    path('decision_tree_play', views.decision_tree_play, name='decision_tree_play'),
]