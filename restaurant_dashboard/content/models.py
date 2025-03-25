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
    RATING_CHOICES = [
        (0, '0 Stars'),
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    # Only customer name is mandatory
    name = models.CharField(max_length=100)  # Customer name
    
    # Optional fields
    content = models.TextField(blank=True, null=True)  # Comments
    is_active = models.BooleanField(default=True)  # Status
    branch = models.ForeignKey('management.Branch', on_delete=models.SET_NULL, 
                               related_name='testimonials', blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # Link to source or profile
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)  # 0-5 stars
    
    # Multiple microsites relationship (already exists)
    microsites = models.ManyToManyField('microsites.Microsite', related_name='testimonials', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"# content/models.py (Update these models)

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
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    # Only name/title is mandatory
    name = models.CharField(max_length=100)  # Title
    
    # Optional fields
    department = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey('management.Branch', on_delete=models.SET_NULL, 
                               related_name='careers', blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, 
                                blank=True, null=True)
        # Changed from URLField to CharField
    url = models.CharField(max_length=255, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Status
    microsites = models.ManyToManyField('microsites.Microsite', related_name='careers', blank=True)
    
    def __str__(self):
        return self.name# content/models.py
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