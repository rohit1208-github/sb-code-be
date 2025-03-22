# microsites/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MicrositeViewSet

router = DefaultRouter()
router.register(r'', MicrositeViewSet, basename='microsite')

urlpatterns = [
    path('', include(router.urls)),
]