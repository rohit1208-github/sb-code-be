# content/serializers.py
from rest_framework import serializers
from .models import MenuItem, Testimonial, FoodDeliveryEmbed, Career
# content/serializers.py (Update the MenuItemSerializer)

class MenuItemSerializer(serializers.ModelSerializer):
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'microsites', 'name', 'description', 'price', 'currency', 
                  'currency_display', 'image', 'is_active', 'created_at', 'updated_at']
        

            
class TestimonialSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)
    
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'content', 'branch', 'branch_name', 
                 'link', 'rating', 'rating_display', 'is_active', 
                 'microsites', 'created_at']
        extra_kwargs = {
            'name': {'required': True},
            'content': {'required': False},
            'branch': {'required': False},
            'link': {'required': False},
            'rating': {'required': False},
            'is_active': {'required': False},
            'microsites': {'required': False},
        }
# content/serializers.py (Update these serializers)

class FoodDeliveryEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDeliveryEmbed
        fields = ['id', 'microsites', 'name', 'url', 'description', 'is_active']

class CareerSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    
    class Meta:
        model = Career
        fields = ['id', 'name', 'department', 'branch', 'branch_name', 'job_type', 
                 'job_type_display', 'url', 'description', 'is_active', 'microsites']
        extra_kwargs = {
            'name': {'required': True},
            'department': {'required': False},
            'branch': {'required': False},
            'job_type': {'required': False},
            'url': {'required': False},
            'description': {'required': False},
            'is_active': {'required': False},
            'microsites': {'required': False},
        }