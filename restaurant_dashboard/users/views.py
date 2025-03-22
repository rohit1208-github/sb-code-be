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

class UserRoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
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