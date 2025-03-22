# microsites/admin.py
from django.contrib import admin
from .models import Microsite, MicrositeSection

class MicrositeSectionInline(admin.TabularInline):
    model = MicrositeSection
    extra = 1

@admin.register(Microsite)
class MicrositeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'has_language_switcher', 'created_at')
    list_filter = ('is_active', 'has_language_switcher')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('branches',)
    inlines = [MicrositeSectionInline]

@admin.register(MicrositeSection)
class MicrositeSectionAdmin(admin.ModelAdmin):
    list_display = ('microsite', 'section_type', 'display_order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('microsite__name',)
    ordering = ('microsite', 'display_order')