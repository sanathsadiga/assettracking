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
        ('inactive', 'Inactive'),
    ]
    
    ANTIVIRUS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    # Asset ID (can be manually entered or auto-generated)
    asset_id = models.CharField(max_length=50, unique=True, db_index=True)
    asset_id_auto_generated = models.BooleanField(default=False, help_text="Was asset_id automatically generated?")
    
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
    po_number = models.CharField(max_length=100, blank=True, null=True, help_text="Purchase Order Number")
    invoice_number = models.CharField(max_length=100, blank=True, null=True, help_text="Invoice Number")
    finance_asset_code = models.CharField(max_length=100, blank=True, null=True, help_text="Finance Asset Code")
    
    # Laptop/Desktop Specific Fields
    cpu_make = models.CharField(max_length=100, blank=True, null=True, help_text="CPU Manufacturer (Intel, AMD, etc.)")
    model = models.CharField(max_length=200, blank=True, null=True, help_text="Device Model")
    processor = models.TextField(blank=True, null=True, help_text="Processor Details (e.g., Intel Core i7-12700K, AMD Ryzen 9 5950X)")
    ram = models.CharField(max_length=50, blank=True, null=True, help_text="RAM (e.g., 8GB, 16GB)")
    hdd = models.CharField(max_length=100, blank=True, null=True, help_text="Hard Drive/Storage")
    os = models.TextField(blank=True, null=True, help_text="Operating System (detailed version info)")
    ms_office_version = models.TextField(blank=True, null=True, help_text="MS Office Version (e.g., MICROSOFT-OFFICE VERSION-7, MICROSOFT-OFFICE VERSION-O365)")
    ip_address = models.CharField(max_length=50, blank=True, null=True, help_text="IP Address")
    hostname = models.CharField(max_length=100, blank=True, null=True, help_text="Hostname")
    
    # Software/Tools
    e1_user = models.BooleanField(default=False, help_text="E1 User")
    e3_user = models.BooleanField(default=False, help_text="E3 User")
    antivirus = models.CharField(max_length=5, choices=ANTIVIRUS_CHOICES, default='no', help_text="Antivirus Installed")
    srilipi = models.BooleanField(default=False, help_text="SRILIPI installed")
    photoshop = models.BooleanField(default=False, help_text="Adobe Photoshop")
    indesign = models.BooleanField(default=False, help_text="Adobe InDesign")
    illustrator = models.BooleanField(default=False, help_text="Adobe Illustrator")
    corel_draw = models.BooleanField(default=False, help_text="CorelDRAW")
    distiller = models.BooleanField(default=False, help_text="Distiller")
    newswrap = models.BooleanField(default=False, help_text="Newswrap")
    
    # User Information
    idm_role = models.CharField(max_length=100, blank=True, null=True, help_text="IDM Role")
    username = models.CharField(max_length=100, blank=True, null=True, help_text="Username")
    official_email = models.EmailField(blank=True, null=True, help_text="Official Email ID")
    sap_id = models.CharField(max_length=100, blank=True, null=True, help_text="SAP ID")
    
    # Warranty & Maintenance
    installation_date = models.DateField(blank=True, null=True, help_text="Installation Date")
    warranty_expiry_date = models.DateField(blank=True, null=True, help_text="Warranty Expiry Date")
    
    # Status & Remarks
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    remarks = models.TextField(blank=True, null=True, help_text="Additional remarks/comments")
    
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

    @classmethod
    def get_unique_os_list(cls):
        """Get list of unique OS entries from database"""
        return (cls.objects.filter(os__isnull=False)
                .exclude(os='')
                .values_list('os', flat=True)
                .distinct()
                .order_by('os'))

    @classmethod
    def get_unique_ms_office_list(cls):
        """Get list of unique MS Office versions from database"""
        return (cls.objects.filter(ms_office_version__isnull=False)
                .exclude(ms_office_version='')
                .values_list('ms_office_version', flat=True)
                .distinct()
                .order_by('ms_office_version'))

    @classmethod
    def get_unique_processor_list(cls):
        """Get list of unique processor entries from database"""
        return (cls.objects.filter(processor__isnull=False)
                .exclude(processor='')
                .values_list('processor', flat=True)
                .distinct()
                .order_by('processor'))

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
