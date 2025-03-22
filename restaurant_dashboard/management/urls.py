# management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]