# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'roles', UserRoleViewSet, basename='user-role')
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]