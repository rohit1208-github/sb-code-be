# management/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Country, Branch
from .serializers import CountrySerializer, BranchSerializer
from users.permissions import IsLeadershipTeam, IsCountryLeadership

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Leadership team can see all countries
        if user.role and user.role.name == 'leadership':
            return Country.objects.all()
        
        # Country leadership & admins can only see their country
        if user.role and user.role.name in ['country_leadership', 'country_admin']:
            if user.country:
                return Country.objects.filter(id=user.country.id)
        
        # Branch managers can only see their branch's country
        if user.role and user.role.name == 'branch_manager':
            if user.branch and user.branch.country:
                return Country.objects.filter(id=user.branch.country.id)
        
        return Country.objects.none()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsLeadershipTeam]
        return [permission() for permission in permission_classes]

class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Leadership team can see all branches
        if user.role and user.role.name == 'leadership':
            return Branch.objects.all()
        
        # Country leadership & admins can only see branches in their country
        if user.role and user.role.name in ['country_leadership', 'country_admin']:
            if user.country:
                return Branch.objects.filter(country=user.country)
        
        # Branch managers can only see their branch
        if user.role and user.role.name == 'branch_manager':
            if user.branch:
                return Branch.objects.filter(id=user.branch.id)
        
        return Branch.objects.none()