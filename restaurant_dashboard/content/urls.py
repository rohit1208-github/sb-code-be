# content/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuItemViewSet, TestimonialViewSet,
    FoodDeliveryEmbedViewSet, CareerViewSet
)

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet, basename='menu-item')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'food-delivery-embeds', FoodDeliveryEmbedViewSet, basename='food-delivery-embed')
router.register(r'careers', CareerViewSet, basename='career')

urlpatterns = [
    path('', include(router.urls)),
]