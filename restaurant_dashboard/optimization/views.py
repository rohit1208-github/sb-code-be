# optimization/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import WhatsAppLink, BaseSEO
from .serializers import WhatsAppLinkSerializer, BaseSEOSerializer
from users.models import User  # Import from users app instead
from users.permissions import IsLeadershipTeam, IsCountryLeadership, IsCountryAdmin

class WhatsAppLinkViewSet(viewsets.ModelViewSet):
    serializer_class = WhatsAppLinkSerializer
    
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

class BaseSEOViewSet(viewsets.ModelViewSet):
    serializer_class = BaseSEOSerializer
    queryset = BaseSEO.objects.all()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsLeadershipTeam]
        return [permission() for permission in permission_classes]