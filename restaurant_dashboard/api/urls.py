# api/urls.py
from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('management/', include('management.urls')),
    path('microsites/', include('microsites.urls')),
    path('content/', include('content.urls')),
    path('optimization/', include('optimization.urls')),
    path('analytics/', include('analytics.urls')),
]