# api/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

# api/urls.py (updated)
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserInfoView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('users/', include('users.urls')),
    path('management/', include('management.urls')),
    path('microsites/', include('microsites.urls')),
    path('content/', include('content.urls')),
    path('optimization/', include('optimization.urls')),
    path('analytics/', include('analytics.urls')),
]
# api/views.py (update existing file)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.urls import get_resolver

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_root(request):
    """
    API documentation root endpoint providing information about available endpoints.
    """
    return Response({
        'management': {
            'countries': request.build_absolute_uri('/api/management/countries/'),
            'branches': request.build_absolute_uri('/api/management/branches/'),
        },
        'users': {
            'users': request.build_absolute_uri('/api/users/'),
            'roles': request.build_absolute_uri('/api/users/roles/'),
        },
        'microsites': {
            'microsites': request.build_absolute_uri('/api/microsites/'),
        },
        'content': {
            'menu_items': request.build_absolute_uri('/api/content/menu-items/'),
            'testimonials': request.build_absolute_uri('/api/content/testimonials/'),
            'food_delivery_embeds': request.build_absolute_uri('/api/content/food-delivery-embeds/'),
            'careers': request.build_absolute_uri('/api/content/careers/'),
        },
        'optimization': {
            'whatsapp_links': request.build_absolute_uri('/api/optimization/whatsapp-links/'),
            'base_seo': request.build_absolute_uri('/api/optimization/base-seo/'),
        },
        'analytics': {
            'dashboard_stats': request.build_absolute_uri('/api/analytics/dashboard-stats/'),
        },
    })

# Update the api/urls.py to include the root API view
# api/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserInfoView, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
    path('users/', include('users.urls')),
    path('management/', include('management.urls')),
    path('microsites/', include('microsites.urls')),
    path('content/', include('content.urls')),
    path('optimization/', include('optimization.urls')),
    path('analytics/', include('analytics.urls')),
]