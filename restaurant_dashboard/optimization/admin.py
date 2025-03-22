# optimization/admin.py
from django.contrib import admin
from .models import WhatsAppLink, BaseSEO

@admin.register(WhatsAppLink)
class WhatsAppLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'branch', 'is_active')
    list_filter = ('is_active', 'branch__country')
    search_fields = ('name', 'phone_number')
    ordering = ('name',)

@admin.register(BaseSEO)
class BaseSEOAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'meta_title')
    search_fields = ('site_name', 'meta_title', 'meta_description')