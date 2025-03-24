# content/models.py
from django.db import models
from microsites.models import Microsite

# class MenuItem(models.Model):
#     microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='menu_items')
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name

class Testimonial(models.Model):
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"
# content/models.py (Update these models)

class FoodDeliveryEmbed(models.Model):
    # Change to ManyToManyField for multiple microsites
    microsites = models.ManyToManyField(Microsite, related_name='food_delivery_embeds')
    name = models.CharField(max_length=100)  # Only this is mandatory
    url = models.URLField(blank=True, null=True)  # Optional
    description = models.TextField(blank=True, null=True)  # Optional
    # embed_code removed as requested
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Career(models.Model):
    # Change to ManyToManyField for multiple microsites
    microsites = models.ManyToManyField(Microsite, related_name='careers')
    name = models.CharField(max_length=100)  # Only this is mandatory
    url = models.URLField(blank=True, null=True)  # Optional (changed from external_url)
    description = models.TextField(blank=True, null=True)  # Optional
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
# content/models.py
from django.db import models
from microsites.models import Microsite
from utils.image_utils import resize_image

# First define all your models correctly
class MenuItem(models.Model):
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee'),
        ('USD', 'US Dollar'),
        ('AED', 'UAE Dirham'),
    ]
    
    # Change to ManyToManyField
    microsites = models.ManyToManyField(Microsite, related_name='menu_items', blank=True)
    name = models.CharField(max_length=100)  # Mandatory
    description = models.TextField(blank=True, null=True)  # Optional
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price field
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD', blank=True, null=True)  # Currency field
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)  # Optional
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