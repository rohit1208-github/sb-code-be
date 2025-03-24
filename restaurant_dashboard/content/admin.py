# content/admin.py
from django.contrib import admin
from .models import MenuItem, Testimonial, FoodDeliveryEmbed, Career
# content/admin.py (Update the MenuItemAdmin)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_microsites', 'price', 'currency', 'is_active', 'created_at')
    list_filter = ('is_active', 'currency')
    search_fields = ('name', 'description')
    filter_horizontal = ('microsites',)  # For easier management of many-to-many
    
    def get_microsites(self, obj):
        return ", ".join([m.name for m in obj.microsites.all()])
    get_microsites.short_description = 'Microsites'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'microsite', 'is_active', 'created_at')
    list_filter = ('is_active', 'microsite')
    search_fields = ('name', 'content')
    ordering = ('microsite', 'created_at')
# content/admin.py (Update these admin classes)

@admin.register(FoodDeliveryEmbed)
class FoodDeliveryEmbedAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_microsites', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('microsites',)  # For easier management of many-to-many
    
    def get_microsites(self, obj):
        return ", ".join([m.name for m in obj.microsites.all()])
    get_microsites.short_description = 'Microsites'

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_microsites', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('microsites',)  # For easier management of many-to-many
    
    def get_microsites(self, obj):
        return ", ".join([m.name for m in obj.microsites.all()])
    get_microsites.short_description = 'Microsites'