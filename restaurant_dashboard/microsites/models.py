# microsites/models.py
from django.db import models
from management.models import Branch

class Microsite(models.Model):
    name = models.CharField(max_length=100)  # Only this is mandatory
    branches = models.ManyToManyField(Branch, related_name='microsites', blank=True)  # Optional multiple branches
    site_id = models.SlugField(unique=True, blank=True, null=True)  # Renamed from 'slug' to 'site_id' and made optional
    is_active = models.BooleanField(default=True, blank=True, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # has_language_switcher and secondary_language fields removed
    
    def __str__(self):
        return self.name

class MicrositeSection(models.Model):
    MENU = 'menu'
    TESTIMONIALS = 'testimonials'
    LOCATION = 'location'
    CONTACT = 'contact'
    ABOUT = 'about'
    
    SECTION_TYPES = [
        (MENU, 'Menu'),
        (TESTIMONIALS, 'Testimonials'),
        (LOCATION, 'Location'),
        (CONTACT, 'Contact'),
        (ABOUT, 'About'),
    ]
    
    microsite = models.ForeignKey(Microsite, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order']
        unique_together = ['microsite', 'section_type']
    
    def __str__(self):
        return f"{self.microsite.name} - {self.get_section_type_display()}"