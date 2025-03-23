# optimization/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import WhatsAppLink, BaseSEO
from .serializers import WhatsAppLinkSerializer, BaseSEOSerializer
from users.models import User  # Import from users app instead
from users.permissions import IsLeadershipTeam, IsCountryLeadership, IsCountryAdmin
# Add these imports
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

@extend_schema_view(
    list=extend_schema(
        summary="List WhatsApp links",
        description="Returns a list of WhatsApp links filtered by user's role and permissions",
        tags=["Optimization"]
    ),
    retrieve=extend_schema(
        summary="Get WhatsApp link details",
        description="Retrieve details of a specific WhatsApp link",
        tags=["Optimization"]
    ),
    create=extend_schema(
        summary="Create WhatsApp link",
        description="Create a new WhatsApp link (restricted by role permissions)",
        tags=["Optimization"]
    ),
    update=extend_schema(
        summary="Update WhatsApp link",
        description="Update all fields of an existing WhatsApp link (restricted by role permissions)",
        tags=["Optimization"]
    ),
    partial_update=extend_schema(
        summary="Partially update WhatsApp link",
        description="Update specific fields of an existing WhatsApp link (restricted by role permissions)",
        tags=["Optimization"]
    ),
    destroy=extend_schema(
        summary="Delete WhatsApp link",
        description="Delete an existing WhatsApp link (restricted by role permissions)",
        tags=["Optimization"]
    )
)
class WhatsAppLinkViewSet(viewsets.ModelViewSet):
    serializer_class = WhatsAppLinkSerializer
    
    @extend_schema(
        description="Returns WhatsApp links based on user's role permissions",
        tags=["Optimization"]
    )
    def get_queryset(self):
        user = self.request.user
        
        # Leadership team can see all WhatsApp links
        if user.role and user.role.name == 'leadership':
            return WhatsAppLink.objects.all()
        
        # Country leadership & admins can only see WhatsApp links for branches in their country
        if user.role and user.role.name in ['country_leadership', 'country_admin']:
            if user.country:
                return WhatsAppLink.objects.filter(
                    Q(branch__country=user.country) | Q(branch__isnull=True)
                )
        
        # Branch managers can only see WhatsApp links for their branch
        if user.role and user.role.name == 'branch_manager':
            if user.branch:
                return WhatsAppLink.objects.filter(
                    Q(branch=user.branch) | Q(branch__isnull=True)
                )
        
        return WhatsAppLink.objects.none()

@extend_schema_view(
    list=extend_schema(
        summary="List SEO configurations",
        description="Returns a list of base SEO configurations",
        tags=["Optimization"]
    ),
    retrieve=extend_schema(
        summary="Get SEO configuration details",
        description="Retrieve details of a specific SEO configuration",
        tags=["Optimization"]
    ),
    create=extend_schema(
        summary="Create SEO configuration",
        description="Create a new SEO configuration (restricted to leadership team)",
        tags=["Optimization"]
    ),
    update=extend_schema(
        summary="Update SEO configuration",
        description="Update all fields of an existing SEO configuration (restricted to leadership team)",
        tags=["Optimization"]
    ),
    partial_update=extend_schema(
        summary="Partially update SEO configuration",
        description="Update specific fields of an existing SEO configuration (restricted to leadership team)",
        tags=["Optimization"]
    ),
    destroy=extend_schema(
        summary="Delete SEO configuration",
        description="Delete an existing SEO configuration (restricted to leadership team)",
        tags=["Optimization"]
    )
)
class BaseSEOViewSet(viewsets.ModelViewSet):
    serializer_class = BaseSEOSerializer
    queryset = BaseSEO.objects.all()
    
    @extend_schema(
        description="Determines permissions based on action and user role",
        tags=["Optimization"]
    )
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsLeadershipTeam]
        return [permission() for permission in permission_classes]