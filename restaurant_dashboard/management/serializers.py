# management/serializers.py
from rest_framework import serializers
from .models import Country, Branch

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code', 'is_active', 'created_at', 'updated_at']

class BranchSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'country', 'country_name', 'address', 'phone', 
                  'email', 'is_active', 'has_online_ordering', 'created_at', 'updated_at']