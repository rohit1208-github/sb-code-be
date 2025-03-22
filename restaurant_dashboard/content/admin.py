# content/admin.py
from django.contrib import admin
from .models import MenuItem, Testimonial, FoodDeliveryEmbed, Career

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'microsite', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'microsite')
    search_fields = ('name', 'description')
    ordering = ('microsite', 'name')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'microsite', 'is_active', 'created_at')
    list_filter = ('is_active', 'microsite')
    search_fields = ('name', 'content')
    ordering = ('microsite', 'created_at')

@admin.register(FoodDeliveryEmbed)
class FoodDeliveryEmbedAdmin(admin.ModelAdmin):
    list_display = ('microsite', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('microsite__name',)

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'microsite', 'external_url', 'is_active')
    list_filter = ('is_active', 'microsite')
    search_fields = ('title',)
    ordering = ('microsite', 'title')