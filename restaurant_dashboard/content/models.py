# content/models.py
from django.db import models
from microsites.models import Microsite

class MenuItem(models.Model):
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"

class FoodDeliveryEmbed(models.Model):
    microsite = models.OneToOneField(Microsite, on_delete=models.CASCADE, related_name='food_delivery_embed')
    embed_code = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Food Delivery Embed for {self.microsite.name}"

class Career(models.Model):
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='careers')
    title = models.CharField(max_length=100)
    external_url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    # content/models.py (update the MenuItem model)
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from utils.image_utils import resize_image

class MenuItem(models.Model):
    # Add these fields if they don't exist
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Resize image if one is provided
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image, max_size=(800, 600))
        super(MenuItem, self).save(*args, **kwargs)