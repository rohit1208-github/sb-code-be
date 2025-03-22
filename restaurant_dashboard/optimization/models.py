# optimization/models.py
from django.db import models
from microsites.models import Microsite
from management.models import Branch

class WhatsAppLink(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    custom_message = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='whatsapp_links', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def get_link(self):
        base_url = "https://wa.me/"
        phone = self.phone_number.replace('+', '').replace(' ', '')
        
        if self.custom_message:
            from urllib.parse import quote
            return f"{base_url}{phone}?text={quote(self.custom_message)}"
        
        return f"{base_url}{phone}"

class BaseSEO(models.Model):
    site_name = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=60)
    meta_description = models.TextField(max_length=160)
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = "Base SEO Configuration"
        verbose_name_plural = "Base SEO Configuration"