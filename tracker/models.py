"""
Models for Asset Tracking System
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Category(models.Model):
    """Asset Category Model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    """Location/Department Model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    """Department/Team Model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Asset(models.Model):
    """Main Asset Model"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('repair', 'Under Repair'),
        ('retired', 'Retired'),
    ]

    # Auto-generated Asset ID (e.g., ASSET0001)
    asset_id = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Barcode (same as asset_id for simplicity)
    barcode = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Asset Details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='assets')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='assets')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    # Financial Information
    purchase_date = models.DateField(blank=False, null=False, default='2026-03-23', help_text="Date when the asset was purchased")
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False, default=0, help_text="Original purchase cost")
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Annual depreciation rate in percentage (e.g., 5 for 5%)")
    current_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Current calculated value after depreciation")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assets_created')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset_id']),
            models.Index(fields=['barcode']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.asset_id} - {self.name}"

    def calculate_depreciation(self):
        """Calculate current value based on depreciation from purchase date"""
        from datetime import datetime
        from decimal import Decimal
        
        if not self.purchase_cost or not self.purchase_date or self.depreciation_rate == 0:
            return self.purchase_cost
        
        # Calculate years elapsed since purchase
        today = datetime.now().date()
        years_elapsed = (today - self.purchase_date).days / 365.25
        
        if years_elapsed <= 0:
            return self.purchase_cost
        
        # Calculate depreciation: Cost * (1 - rate)^years
        rate = Decimal(str(self.depreciation_rate)) / Decimal('100')
        base_value = Decimal(str(self.purchase_cost))
        depreciated_value = base_value * ((Decimal('1') - rate) ** Decimal(str(years_elapsed)))
        
        return round(depreciated_value, 2)

    def save(self, *args, **kwargs):
        """Override save to auto-generate asset_id and barcode if not exists"""
        if not self.asset_id:
            # Generate unique asset ID
            count = Asset.objects.count()
            self.asset_id = f"ASSET{count + 1:04d}"
        
        if not self.barcode:
            self.barcode = self.asset_id
        
        # Calculate and update current value if financial info is provided
        if self.purchase_cost and self.purchase_date:
            self.current_value = self.calculate_depreciation()
        
        super().save(*args, **kwargs)


class AssetLog(models.Model):
    """Audit Log for Asset Actions"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('unassigned', 'Unassigned'),
        ('status_changed', 'Status Changed'),
        ('location_changed', 'Location Changed'),
        ('scanned', 'Scanned'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='asset_actions')
    
    # Change tracking
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['asset', '-timestamp']),
            models.Index(fields=['performed_by', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.asset.asset_id} - {self.action} - {self.timestamp}"
