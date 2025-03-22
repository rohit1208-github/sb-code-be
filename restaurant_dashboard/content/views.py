# content/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Testimonial, FoodDeliveryEmbed, Career
from .serializers import (
    MenuItemSerializer, TestimonialSerializer,
    FoodDeliveryEmbedSerializer, CareerSerializer
)
from users.permissions import IsLeadershipTeam, IsCountryLeadership, IsCountryAdmin, IsBranchManager
from django.db.models import Q

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Filter by microsite if provided
        microsite_id = self.request.query_params.get('microsite', None)
        base_queryset = MenuItem.objects.all()
        
        if microsite_id:
            base_queryset = base_queryset.filter(microsite_id=microsite_id)
        
        # Leadership team can see all menu items
        if hasattr(user, 'role') and user.role and user.role.name == 'leadership':
            return base_queryset
        
        # Country leadership & admins can only see menu items for microsites in their country
        if hasattr(user, 'role') and user.role and user.role.name in ['country_leadership', 'country_admin']:
            if hasattr(user, 'country') and user.country:
                return base_queryset.filter(microsite__branches__country=user.country).distinct()
        
        # Branch managers can only see menu items for microsites linked to their branch
        if hasattr(user, 'role') and user.role and user.role.name == 'branch_manager':
            if hasattr(user, 'branch') and user.branch:
                return base_queryset.filter(microsite__branches=user.branch)
        
        return MenuItem.objects.none()
    
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

class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Filter by microsite if provided
        microsite_id = self.request.query_params.get('microsite', None)
        base_queryset = Testimonial.objects.all()
        
        if microsite_id:
            base_queryset = base_queryset.filter(microsite_id=microsite_id)
        
        # Leadership team can see all testimonials
        if user.role and user.role.name == 'leadership':
            return base_queryset
        
        # Country leadership & admins can only see testimonials for microsites in their country
        if user.role and user.role.name in ['country_leadership', 'country_admin']:
            if user.country:
                return base_queryset.filter(microsite__branches__country=user.country).distinct()
        
        # Branch managers can only see testimonials for microsites linked to their branch
        if user.role and user.role.name == 'branch_manager':
            if user.branch:
                return base_queryset.filter(microsite__branches=user.branch)
        
        return Testimonial.objects.none()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.role and self.request.user.role.name in ['leadership', 'country_leadership', 'country_admin']:
                permission_classes = [IsAuthenticated]
            else:
                permission_classes = [IsBranchManager]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class FoodDeliveryEmbedViewSet(viewsets.ModelViewSet):
    serializer_class = FoodDeliveryEmbedSerializer
    
    def get_queryset(self):
        # Similar permission logic as other viewsets
        user = self.request.user
        
        # Filter by microsite
        microsite_id = self.request.query_params.get('microsite', None)
        base_queryset = FoodDeliveryEmbed.objects.all()
        
        if microsite_id:
            base_queryset = base_queryset.filter(microsite_id=microsite_id)
        
        # Apply role-based filtering
        if user.role.name == 'leadership':
            return base_queryset
        elif user.role.name in ['country_leadership', 'country_admin'] and user.country:
            return base_queryset.filter(microsite__branches__country=user.country).distinct()
        elif user.role.name == 'branch_manager' and user.branch:
            return base_queryset.filter(microsite__branches=user.branch)
        
        return FoodDeliveryEmbed.objects.none()

class CareerViewSet(viewsets.ModelViewSet):
    serializer_class = CareerSerializer
    
    def get_queryset(self):
        # Similar permission logic as other viewsets
        user = self.request.user
        
        # Filter by microsite
        microsite_id = self.request.query_params.get('microsite', None)
        base_queryset = Career.objects.all()
        
        if microsite_id:
            base_queryset = base_queryset.filter(microsite_id=microsite_id)
        
        # Apply role-based filtering
        if user.role.name == 'leadership':
            return base_queryset
        elif user.role.name in ['country_leadership', 'country_admin'] and user.country:
            return base_queryset.filter(microsite__branches__country=user.country).distinct()
        elif user.role.name == 'branch_manager' and user.branch:
            return base_queryset.filter(microsite__branches=user.branch)
        
        return Career.objects.none()
    # content/views.py (add to existing file)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os

class MenuItemViewSet(viewsets.ModelViewSet):
    # Add to existing class
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        if 'file' not in request.data:
            return Response({'error': 'No file was provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.data['file']
        menu_item_id = request.data.get('menu_item_id')
        
        if not menu_item_id:
            return Response({'error': 'Menu item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
            
            # Check if user has permission to update this menu item
            self.check_object_permissions(request, menu_item)
            
            # Delete old image if it exists
            if menu_item.image and os.path.isfile(menu_item.image.path):
                os.remove(menu_item.image.path)
            
            menu_item.image = file
            menu_item.save()
            
            return Response(
                MenuItemSerializer(menu_item).data,
                status=status.HTTP_200_OK
            )
            
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        