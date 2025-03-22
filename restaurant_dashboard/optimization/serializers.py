# optimization/serializers.py
from rest_framework import serializers
from .models import WhatsAppLink, BaseSEO

class WhatsAppLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    
    class Meta:
        model = WhatsAppLink
        fields = ['id', 'name', 'phone_number', 'custom_message', 'branch', 'is_active', 'link']
    
    def get_link(self, obj):
        return obj.get_link()

class BaseSEOSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSEO
        fields = ['id', 'site_name', 'meta_title', 'meta_description', 
                  'favicon', 'og_image', 'google_analytics_id']