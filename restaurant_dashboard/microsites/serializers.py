# microsites/serializers.py
from rest_framework import serializers
from .models import Microsite, MicrositeSection
from management.models import Branch
from management.serializers import BranchSerializer

class MicrositeSectionSerializer(serializers.ModelSerializer):
    section_type_display = serializers.CharField(source='get_section_type_display', read_only=True)
    
    class Meta:
        model = MicrositeSection
        fields = ['id', 'section_type', 'section_type_display', 'display_order', 'is_active']

class MicrositeSerializer(serializers.ModelSerializer):
    sections = MicrositeSectionSerializer(many=True, read_only=True)
    branches_data = BranchSerializer(source='branches', many=True, read_only=True)
    
    class Meta:
        model = Microsite
        fields = ['id', 'name', 'site_id', 'branches', 'branches_data', 'is_active',
                  'sections', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        branches_data = validated_data.pop('branches', [])
        microsite = Microsite.objects.create(**validated_data)
        
        for branch_data in branches_data:
            try:
                # Handle the case when branch_data is a Branch object
                if hasattr(branch_data, 'id'):
                    branch_id = branch_data.id
                else:
                    branch_id = branch_data
                    
                branch = Branch.objects.get(id=branch_id)
                microsite.branches.add(branch)
            except (Branch.DoesNotExist, AttributeError, ValueError, TypeError):
                # Skip invalid branches
                continue
        
        # Create default sections
        default_sections = [
            {'section_type': MicrositeSection.MENU, 'display_order': 1},
            {'section_type': MicrositeSection.TESTIMONIALS, 'display_order': 2},
            {'section_type': MicrositeSection.LOCATION, 'display_order': 3},
            {'section_type': MicrositeSection.CONTACT, 'display_order': 4},
            {'section_type': MicrositeSection.ABOUT, 'display_order': 5},
        ]
        
        for section in default_sections:
            MicrositeSection.objects.create(microsite=microsite, **section)
        
        return microsite