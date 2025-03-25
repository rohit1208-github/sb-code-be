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
# Add these imports
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os

@extend_schema_view(
    list=extend_schema(
        summary="List menu items",
        description="Returns a list of menu items filtered by user's role and permissions",
        parameters=[
            OpenApiParameter(name="microsite", description="Filter by microsite ID (optional)", required=False, type=int)
        ],
        tags=["Content Management"]
    ),
    retrieve=extend_schema(
        summary="Get menu item details",
        description="Retrieve details of a specific menu item",
        tags=["Content Management"]
    ),
    create=extend_schema(
        summary="Create menu item",
        description="Create a new menu item (restricted by role permissions)",
        tags=["Content Management"]
    ),
    update=extend_schema(
        summary="Update menu item",
        description="Update all fields of an existing menu item (restricted by role permissions)",
        tags=["Content Management"]
    ),
    partial_update=extend_schema(
        summary="Partially update menu item",
        description="Update specific fields of an existing menu item (restricted by role permissions)",
        tags=["Content Management"]
    ),
    destroy=extend_schema(
        summary="Delete menu item",
        description="Delete an existing menu item (restricted by role permissions)",
        tags=["Content Management"]
    )
)
class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def get_queryset(self):
        user = self.request.user
        
        # Filter by microsite if provided (optional parameter)
        microsite_id = self.request.query_params.get('microsite', None)
        base_queryset = MenuItem.objects.all()
        
        if microsite_id:
            base_queryset = base_queryset.filter(microsites__id=microsite_id)
        
        # Leadership team can see all menu items
        if hasattr(user, 'role') and user.role and user.role.name == 'leadership':
            return base_queryset
        
        # Country leadership & admins can only see menu items for microsites in their country
        if hasattr(user, 'role') and user.role and user.role.name in ['country_leadership', 'country_admin']:
            if hasattr(user, 'country') and user.country:
                return base_queryset.filter(microsites__branches__country=user.country).distinct()
        
        # Branch managers can only see menu items for microsites linked to their branch
        if hasattr(user, 'role') and user.role and user.role.name == 'branch_manager':
            if hasattr(user, 'branch') and user.branch:
                return base_queryset.filter(microsites__branches=user.branch).distinct()
        
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
    
    @extend_schema(
        summary="Upload menu item image",
        description="Upload an image for a specific menu item",
        request={"multipart/form-data": {"file": "file", "menu_item_id": "string"}},
        responses={
            200: MenuItemSerializer,
            400: OpenApiResponse(description="Bad request: missing file or menu item ID"),
            404: OpenApiResponse(description="Menu item not found"),
            500: OpenApiResponse(description="Internal server error")
        },
        tags=["Content Management"]
    )
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

@extend_schema_view(
    list=extend_schema(
        summary="List testimonials",
        description="Returns a list of testimonials filtered by user's role and permissions",
        parameters=[
            OpenApiParameter(name="microsite", description="Filter by microsite ID (optional)", required=False, type=int),
            OpenApiParameter(name="branch", description="Filter by branch ID (optional)", required=False, type=int)
        ],
        tags=["Content Management"]
    ),
    retrieve=extend_schema(
        summary="Get testimonial details",
        description="Retrieve details of a specific testimonial",
        tags=["Content Management"]
    ),
    create=extend_schema(
        summary="Create testimonial",
        description="Create a new testimonial (restricted by role permissions)",
        tags=["Content Management"]
    ),
    update=extend_schema(
        summary="Update testimonial",
        description="Update all fields of an existing testimonial (restricted by role permissions)",
        tags=["Content Management"]
    ),
    partial_update=extend_schema(
        summary="Partially update testimonial",
        description="Update specific fields of an existing testimonial (restricted by role permissions)",
        tags=["Content Management"]
    ),
    destroy=extend_schema(
        summary="Delete testimonial",
        description="Delete an existing testimonial (restricted by role permissions)",
        tags=["Content Management"]
    )
)
class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    
    def get_queryset(self):
        user = self.request.user
        base_queryset = Testimonial.objects.all()
        
        # Filter by microsite if provided
        microsite_id = self.request.query_params.get('microsite', None)
        if microsite_id:
            base_queryset = base_queryset.filter(microsites__id=microsite_id)
            
        # Filter by branch if provided
        branch_id = self.request.query_params.get('branch', None)
        if branch_id:
            base_queryset = base_queryset.filter(branch_id=branch_id)
        
        # Apply role-based filtering (existing logic)
        if hasattr(user, 'role') and user.role:
            if user.role.name == 'leadership':
                return base_queryset
            elif user.role.name in ['country_leadership', 'country_admin'] and hasattr(user, 'country') and user.country:
                return base_queryset.filter(microsites__branches__country=user.country).distinct()
            elif user.role.name == 'branch_manager' and hasattr(user, 'branch') and user.branch:
                return base_queryset.filter(microsites__branches=user.branch).distinct()
        
        return Testimonial.objects.none()
    
    # Add an endpoint to get available branches
    @extend_schema(
        summary="Get available branches",
        description="Returns a list of branches available for testimonials",
        responses={200: OpenApiResponse(description="List of available branches")},
        tags=["Content Management"]
    )
    @action(detail=False, methods=['get'])
    def available_branches(self, request):
        from management.models import Branch
        from management.serializers import BranchSerializer
        
        user = request.user
        branches = []
        
        if user.role and user.role.name == 'leadership':
            branches = Branch.objects.filter(is_active=True)
        elif user.role and user.role.name in ['country_leadership', 'country_admin'] and user.country:
            branches = Branch.objects.filter(country=user.country, is_active=True)
        elif user.role and user.role.name == 'branch_manager' and user.branch:
            branches = Branch.objects.filter(id=user.branch.id, is_active=True)
            
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)    

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         if self.request.user.role and self.request.user.role.name in ['leadership', 'country_leadership', 'country_admin']:
    #             permission_classes = [IsAuthenticated]
    #         else:
    #             permission_classes = [IsBranchManager]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]

# content/views.py (Update these viewsets)

@extend_schema_view(
    list=extend_schema(
        summary="List food delivery embeds",
        description="Returns a list of food delivery embeds filtered by user's role and permissions",
        parameters=[
            OpenApiParameter(name="microsite", description="Filter by microsite ID (optional)", required=False, type=int)
        ],
        tags=["Content Management"]
    ),
    # Other schema definitions remain the same
)
class FoodDeliveryEmbedViewSet(viewsets.ModelViewSet):
    serializer_class = FoodDeliveryEmbedSerializer
    
    def get_queryset(self):
        user = self.request.user
        base_queryset = FoodDeliveryEmbed.objects.all()
        
        # Filter by microsite if provided (optional parameter)
        microsite_id = self.request.query_params.get('microsite', None)
        if microsite_id:
            base_queryset = base_queryset.filter(microsites__id=microsite_id)
        
        # Apply role-based filtering
        if hasattr(user, 'role') and user.role:
            if user.role.name == 'leadership':
                return base_queryset
            elif user.role.name in ['country_leadership', 'country_admin'] and hasattr(user, 'country') and user.country:
                return base_queryset.filter(microsites__branches__country=user.country).distinct()
            elif user.role.name == 'branch_manager' and hasattr(user, 'branch') and user.branch:
                return base_queryset.filter(microsites__branches=user.branch).distinct()
        
        return FoodDeliveryEmbed.objects.none()

@extend_schema_view(
    list=extend_schema(
        summary="List careers",
        description="Returns a list of careers filtered by user's role and permissions",
        parameters=[
            OpenApiParameter(name="microsite", description="Filter by microsite ID (optional)", required=False, type=int),
            OpenApiParameter(name="branch", description="Filter by branch ID (optional)", required=False, type=int)
        ],
        tags=["Content Management"]
    ),
    # Other schema definitions remain the same
)
class CareerViewSet(viewsets.ModelViewSet):
    serializer_class = CareerSerializer
    
    def get_queryset(self):
        user = self.request.user
        base_queryset = Career.objects.all()
        
        # Filter by microsite if provided (optional parameter)
        microsite_id = self.request.query_params.get('microsite', None)
        if microsite_id:
            base_queryset = base_queryset.filter(microsites__id=microsite_id)
            
        # Filter by branch if provided (optional parameter)
        branch_id = self.request.query_params.get('branch', None)
        if branch_id:
            base_queryset = base_queryset.filter(branch_id=branch_id)
        
        # Apply role-based filtering (existing code...)
        if hasattr(user, 'role') and user.role:
            if user.role.name == 'leadership':
                return base_queryset
            elif user.role.name in ['country_leadership', 'country_admin'] and hasattr(user, 'country') and user.country:
                return base_queryset.filter(microsites__branches__country=user.country).distinct()
            elif user.role.name == 'branch_manager' and hasattr(user, 'branch') and user.branch:
                return base_queryset.filter(microsites__branches=user.branch).distinct()
        
        return Career.objects.none()
    
    # Add an endpoint to get available branches
    @extend_schema(
        summary="Get available branches",
        description="Returns a list of branches available for careers",
        responses={200: OpenApiResponse(description="List of available branches")},
        tags=["Content Management"]
    )
    @action(detail=False, methods=['get'])
    def available_branches(self, request):
        from management.models import Branch
        from management.serializers import BranchSerializer
        
        user = request.user
        branches = []
        
        if user.role and user.role.name == 'leadership':
            branches = Branch.objects.filter(is_active=True)
        elif user.role and user.role.name in ['country_leadership', 'country_admin'] and user.country:
            branches = Branch.objects.filter(country=user.country, is_active=True)
        elif user.role and user.role.name == 'branch_manager' and user.branch:
            branches = Branch.objects.filter(id=user.branch.id, is_active=True)
            
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)