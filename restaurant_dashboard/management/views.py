# management/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Country, Branch
from .serializers import CountrySerializer, BranchSerializer
from users.permissions import IsLeadershipTeam, IsCountryLeadership
# Add these imports
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    list=extend_schema(
        summary="List countries",
        description="Returns a list of countries filtered by user's role and permissions",
        tags=["Management"]
    ),
    retrieve=extend_schema(
        summary="Get country details",
        description="Retrieve details of a specific country",
        tags=["Management"]
    ),
    create=extend_schema(
        summary="Create country",
        description="Create a new country (restricted to leadership team)",
        tags=["Management"]
    ),
    update=extend_schema(
        summary="Update country",
        description="Update all fields of an existing country (restricted to leadership team)",
        tags=["Management"]
    ),
    partial_update=extend_schema(
        summary="Partially update country",
        description="Update specific fields of an existing country (restricted to leadership team)",
        tags=["Management"]
    ),
    destroy=extend_schema(
        summary="Delete country",
        description="Delete an existing country (restricted to leadership team)",
        tags=["Management"]
    )
)
class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    
    @extend_schema(
        description="Returns countries based on user's role permissions",
        tags=["Management"]
    )
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
    
    @extend_schema(
        description="Determines permissions based on action and user role",
        tags=["Management"]
    )
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsLeadershipTeam]
        return [permission() for permission in permission_classes]

@extend_schema_view(
    list=extend_schema(
        summary="List branches",
        description="Returns a list of branches filtered by user's role and permissions",
        tags=["Management"]
    ),
    retrieve=extend_schema(
        summary="Get branch details",
        description="Retrieve details of a specific branch",
        tags=["Management"]
    ),
    create=extend_schema(
        summary="Create branch",
        description="Create a new branch (role-based permissions apply)",
        tags=["Management"]
    ),
    update=extend_schema(
        summary="Update branch",
        description="Update all fields of an existing branch (role-based permissions apply)",
        tags=["Management"]
    ),
    partial_update=extend_schema(
        summary="Partially update branch",
        description="Update specific fields of an existing branch (role-based permissions apply)",
        tags=["Management"]
    ),
    destroy=extend_schema(
        summary="Delete branch",
        description="Delete an existing branch (role-based permissions apply)",
        tags=["Management"]
    )
)
class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    
    @extend_schema(
        description="Returns branches based on user's role permissions",
        tags=["Management"]
    )
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