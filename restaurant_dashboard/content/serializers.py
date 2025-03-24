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
    class Meta:
        model = Testimonial
        fields = ['id', 'microsites', 'name', 'content', 'is_active', 'created_at']

# content/serializers.py (Update these serializers)

class FoodDeliveryEmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDeliveryEmbed
        fields = ['id', 'microsites', 'name', 'url', 'description', 'is_active']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'microsites', 'name', 'url', 'description', 'is_active']