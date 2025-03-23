# analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from management.models import Branch
from content.models import MenuItem
from users.models import User
from microsites.models import Microsite
# Add this import
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from rest_framework import serializers

# Define a response serializer for documentation
class DashboardStatsResponseSerializer(serializers.Serializer):
    statistics = serializers.DictField(
        child=serializers.DictField(),
        help_text="Various statistics about the system"
    )
    recentMenuItems = serializers.ListField(
        child=serializers.DictField(),
        help_text="Recent menu items added to the system"
    )
    staffCount = serializers.IntegerField(help_text="Total number of staff users")
    webTraffic = serializers.DictField(help_text="Web traffic statistics")
    socialMedia = serializers.DictField(help_text="Social media engagement metrics")
    trafficByRegion = serializers.ListField(
        child=serializers.DictField(),
        help_text="Traffic statistics by region"
    )

class DashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get dashboard statistics",
        description="Returns various statistics and metrics for the dashboard including branch data, user counts, web traffic, and social media metrics.",
        tags=["Analytics"],
        responses={
            200: OpenApiResponse(
                response=DashboardStatsResponseSerializer,
                description="Dashboard statistics retrieved successfully"
            ),
            401: OpenApiResponse(description="Authentication failed")
        },
        examples=[
            OpenApiExample(
                "Example Response",
                value={
                    "statistics": {
                        "branchesWithOrdering": {"count": 10, "newLinks": 3},
                        "contactEntries": {"count": 30, "unread": 6},
                        "micrositesLive": {"count": 5, "newToday": 1},
                        "lifetimeVisitors": {"count": 220000, "message": "Lifetime visits across all regions"}
                    },
                    "recentMenuItems": [
                        {"id": 1, "name": "Sample Item", "branch": "Branch Name", "branches": 3, "image": "http://example.com/image.jpg"}
                    ],
                    "staffCount": 25,
                    "webTraffic": {"total": 320958, "growth": 20.9},
                    "socialMedia": {"likes": 306500, "comments": 27500},
                    "trafficByRegion": [{"region": "Region A", "visits": 44}]
                }
            )
        ]
    )
    def get(self, request):
        # Get counts
        total_branches = Branch.objects.count()
        branches_with_ordering = Branch.objects.filter(has_online_ordering=True).count()
        total_staff = User.objects.filter(is_staff=False).count()
        total_microsites = Microsite.objects.filter(is_active=True).count()
        
        # Get recent menu items
        recent_menu_items = []
        menu_items = MenuItem.objects.select_related('microsite').order_by('-created_at')[:5]
        for item in menu_items:
            # Count branches for each menu item
            branches_count = item.microsite.branches.count()
            recent_menu_items.append({
                'id': item.id,
                'name': item.name,
                'branch': item.microsite.name,
                'branches': branches_count,
                'image': request.build_absolute_uri(item.image.url) if item.image else None
            })
        
        # Mock web traffic data
        web_traffic = {
            'total': 320958,
            'growth': 20.9,
            'sources': [
                {'name': 'Direct visit', 'percentage': 42.66, 'color': 'bg-blue-500'},
                {'name': 'Organic Search', 'percentage': 36.80, 'color': 'bg-black'},
                {'name': 'Referral Website', 'percentage': 15.34, 'color': 'bg-yellow-500'},
                {'name': 'Social Networks', 'percentage': 9.20, 'color': 'bg-red-500'}
            ]
        }
        
        # Mock social media data
        social_media = {
            'likes': 306500,
            'comments': 27500
        }
        
        # Mock traffic by region data
        traffic_by_region = [
            {'region': 'Region A', 'visits': 44},
            {'region': 'Region B', 'visits': 55},
            {'region': 'Region C', 'visits': 57},
            {'region': 'Region D', 'visits': 56},
            {'region': 'Region E', 'visits': 61},
            {'region': 'Region F', 'visits': 58},
            {'region': 'Region G', 'visits': 63},
            {'region': 'Region H', 'visits': 60},
            {'region': 'Region I', 'visits': 66}
        ]
        
        # Prepare response data
        data = {
            'statistics': {
                'branchesWithOrdering': {
                    'count': branches_with_ordering,
                    'newLinks': 3  # Mock data
                },
                'contactEntries': {
                    'count': 30,  # Mock data
                    'unread': 6   # Mock data
                },
                'micrositesLive': {
                    'count': total_microsites,
                    'newToday': 1  # Mock data
                },
                'lifetimeVisitors': {
                    'count': 220000,  # Mock data
                    'message': 'Lifetime visits across all regions'
                }
            },
            'recentMenuItems': recent_menu_items,
            'staffCount': total_staff,
            'webTraffic': web_traffic,
            'socialMedia': social_media,
            'trafficByRegion': traffic_by_region
        }
        
        return Response(data, status=status.HTTP_200_OK)