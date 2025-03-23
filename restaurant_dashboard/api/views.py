# api/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
# Add these imports
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import api_view, permission_classes
from django.urls import get_resolver

User = get_user_model()

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get current user information",
        description="Returns information about the currently authenticated user",
        tags=["Authentication"],
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="Authentication failed")
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

@extend_schema(
    summary="API root overview",
    description="API documentation root endpoint providing information about available endpoints",
    tags=["API Documentation"],
    responses={
        200: OpenApiResponse(
            description="Dictionary of available API endpoints organized by app",
            response=dict
        ),
        401: OpenApiResponse(description="Authentication failed")
    }
)
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



# Add these to api/views.py

from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        summary="Obtain JWT token pair",
        description="Takes a set of user credentials and returns an access and refresh JSON web token pair",
        tags=["Authentication"],
        responses={
            200: OpenApiResponse(description="JWT token pair obtained successfully"),
            401: OpenApiResponse(description="Invalid credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="Refresh JWT token",
        description="Takes a refresh type JSON web token and returns an access type JSON web token",
        tags=["Authentication"],
        responses={
            200: OpenApiResponse(description="Token refreshed successfully"),
            401: OpenApiResponse(description="Invalid refresh token")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)