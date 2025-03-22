# # management/admin.py
# from django.contrib import admin
# from .models import Country, Branch

# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code', 'is_active', 'created_at')
#     list_filter = ('is_active',)
#     search_fields = ('name', 'code')
#     ordering = ('name',)

# @admin.register(Branch)
# class BranchAdmin(admin.ModelAdmin):
#     list_display = ('name', 'country', 'is_active', 'has_online_ordering', 'created_at')
#     list_filter = ('is_active', 'has_online_ordering', 'country')
#     search_fields = ('name', 'address', 'email')
#     ordering = ('country', 'name')