from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('pages.urls')),
    path('linear_regression/', include('linear_regression.urls')),
    path('multiple_linear_regression/', include('multiple_linear_regression.urls')),
    path('polynomial_regression/', include('polynomial_regression.urls')),
    path('svr/', include('svr.urls')),
    path('decision_tree/', include('decision_tree.urls')),
    path('random_forest/', include('random_forest.urls')),
    path('admin/', admin.site.urls),
]