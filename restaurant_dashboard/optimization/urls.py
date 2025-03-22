# optimization/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WhatsAppLinkViewSet, BaseSEOViewSet

router = DefaultRouter()
router.register(r'whatsapp-links', WhatsAppLinkViewSet, basename='whatsapp-link')
router.register(r'base-seo', BaseSEOViewSet, basename='base-seo')

urlpatterns = [
    path('', include(router.urls)),
]