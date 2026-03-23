"""
Admin configuration for Asset Tracking System
"""
from django.contrib import admin
from .models import Asset, Category, Location, Department, AssetLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'name', 'category', 'location', 'department', 'status', 'assigned_to', 'current_value', 'created_at']
    list_filter = ['status', 'category', 'location', 'department', 'created_at']
    search_fields = ['asset_id', 'barcode', 'name', 'serial_number']
    readonly_fields = ['asset_id', 'barcode', 'created_at', 'updated_at', 'current_value']
    fieldsets = (
        ('Asset Information', {
            'fields': ('asset_id', 'barcode', 'name', 'description', 'serial_number')
        }),
        ('Classification', {
            'fields': ('category', 'location', 'department')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status')
        }),
        ('Financial Information', {
            'fields': ('purchase_date', 'purchase_cost', 'depreciation_rate', 'current_value'),
            'classes': ('collapse',),
            'description': 'Purchase details and depreciation tracking'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AssetLog)
class AssetLogAdmin(admin.ModelAdmin):
    list_display = ['asset', 'action', 'performed_by', 'timestamp']
    list_filter = ['action', 'timestamp', 'asset__category']
    search_fields = ['asset__asset_id', 'asset__name', 'performed_by__username']
    readonly_fields = ['asset', 'action', 'performed_by', 'timestamp', 'old_value', 'new_value']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
