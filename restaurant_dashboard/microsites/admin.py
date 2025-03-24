# microsites/admin.py
from django.contrib import admin
from .models import Microsite, MicrositeSection

class MicrositeSectionInline(admin.TabularInline):
    model = MicrositeSection
    extra = 1

@admin.register(Microsite)
class MicrositeAdmin(admin.ModelAdmin):
    list_display = ('name', 'site_id', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'site_id')
    prepopulated_fields = {'site_id': ('name',)}
    filter_horizontal = ('branches',)
    inlines = [MicrositeSectionInline]

@admin.register(MicrositeSection)
class MicrositeSectionAdmin(admin.ModelAdmin):
    list_display = ('microsite', 'section_type', 'display_order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('microsite__name',)
    ordering = ('microsite', 'display_order')