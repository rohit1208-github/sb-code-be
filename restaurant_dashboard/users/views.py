# users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserRole
from .serializers import UserSerializer, UserRoleSerializer
# Add these imports
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

@extend_schema_view(
    list=extend_schema(
        summary="List user roles",
        description="Returns a list of all available user roles",
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Get user role details",
        description="Retrieve details of a specific user role",
        tags=["Users"]
    )
)
class UserRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

@extend_schema_view(
    list=extend_schema(
        summary="List users",
        description="Returns a list of users filtered by user's role and permissions",
        tags=["Users"]
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve details of a specific user",
        tags=["Users"]
    ),
    create=extend_schema(
        summary="Create user",
        description="Create a new user (restricted by role permissions)",
        tags=["Users"]
    ),
    update=extend_schema(
        summary="Update user",
        description="Update all fields of an existing user (restricted by role permissions)",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Partially update user",
        description="Update specific fields of an existing user (restricted by role permissions)",
        tags=["Users"]
    ),
    destroy=extend_schema(
        summary="Delete user",
        description="Delete an existing user (restricted by role permissions)",
        tags=["Users"]
    )
)
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    @extend_schema(
        description="Returns users based on the requester's role permissions",
        tags=["Users"]
    )
    def get_queryset(self):
        user = self.request.user
        
        # Leadership team can see all users
        if user.role and user.role.name == 'leadership':
            return User.objects.all()
        
        # Country leadership can see users in their country
        if user.role and user.role.name == 'country_leadership':
            if user.country:
                return User.objects.filter(
                    Q(country=user.country) | 
                    Q(branch__country=user.country)
                ).distinct()
        
        # Country admin can see some users in their country
        if user.role and user.role.name == 'country_admin':
            if user.country:
                return User.objects.filter(
                    Q(country=user.country) | 
                    Q(branch__country=user.country),
                    ~Q(role__name='leadership'),
                    ~Q(role__name='country_leadership')
                ).distinct()
        
        # Branch managers can only see themselves
        if user.role and user.role.name == 'branch_manager':
            return User.objects.filter(id=user.id)
        
        return User.objects.none()