# microsites/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Add this import
from rest_framework.views import APIView

from .models import Microsite, MicrositeSection
from .serializers import MicrositeSerializer, MicrositeSectionSerializer
from users.permissions import IsLeadershipTeam, IsCountryLeadership, IsCountryAdmin, IsBranchManager

class MicrositeViewSet(viewsets.ModelViewSet):
    serializer_class = MicrositeSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Leadership team can see all microsites
        if user.role and user.role.name == 'leadership':
            return Microsite.objects.all()
        
        # Country leadership & admins can only see microsites linked to branches in their country
        if user.role and user.role.name in ['country_leadership', 'country_admin']:
            if user.country:
                return Microsite.objects.filter(branches__country=user.country).distinct()
        
        # Branch managers can only see microsites linked to their branch
        if user.role and user.role.name == 'branch_manager':
            if user.branch:
                return Microsite.objects.filter(branches=user.branch)
        
        return Microsite.objects.none()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.role and self.request.user.role.name == 'leadership':
                permission_classes = [IsLeadershipTeam]
            elif self.request.user.role and self.request.user.role.name == 'country_leadership':
                permission_classes = [IsCountryLeadership]
            else:
                permission_classes = [IsCountryAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get', 'put'])
    def sections(self, request, pk=None):
        microsite = self.get_object()
        
        if request.method == 'GET':
            sections = microsite.sections.all()
            serializer = MicrositeSectionSerializer(sections, many=True)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            # Update section order
            section_data = request.data
            for item in section_data:
                try:
                    section = MicrositeSection.objects.get(id=item['id'], microsite=microsite)
                    section.display_order = item['display_order']
                    section.is_active = item.get('is_active', section.is_active)
                    section.save()
                except MicrositeSection.DoesNotExist:
                    pass
            
            sections = microsite.sections.all()
            serializer = MicrositeSectionSerializer(sections, many=True)
            return Response(serializer.data)