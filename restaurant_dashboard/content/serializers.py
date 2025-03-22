# content/serializers.py
from rest_framework import serializers
from .models import MenuItem, Testimonial, FoodDeliveryEmbed, Career

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'microsite', 'name', 'description', 'price', 'image', 
                  'is_active', 'created_at', 'updated_at']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'microsite', 'name', 'content', 'is_active', 'created_at']

class FoodDeliveryEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDeliveryEmbed
        fields = ['id', 'microsite', 'embed_code', 'is_active']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'microsite', 'title', 'external_url', 'is_active']