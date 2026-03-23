"""
Serializers for Asset Tracking API
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from tracker.models import Asset, Category, Location, AssetLog


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'created_at']


class AssetLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AssetLog
        fields = [
            'id', 'asset', 'action', 'action_display', 'performed_by', 
            'performed_by_name', 'old_value', 'new_value', 'timestamp', 'notes'
        ]
        read_only_fields = ['timestamp']


class AssetListSerializer(serializers.ModelSerializer):
    """Serializer for asset list view"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Asset
        fields = [
            'id', 'asset_id', 'barcode', 'name', 'category', 'category_name',
            'location', 'location_name', 'status', 'status_display',
            'assigned_to', 'assigned_to_name', 'created_at', 'updated_at'
        ]


class AssetDetailSerializer(serializers.ModelSerializer):
    """Serializer for asset detail view with logs"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    logs = AssetLogSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = [
            'id', 'asset_id', 'barcode', 'name', 'description', 'serial_number',
            'category', 'category_name', 'location', 'location_name',
            'status', 'status_display', 'assigned_to', 'assigned_to_name',
            'created_by', 'created_by_name', 'created_at', 'updated_at', 'logs'
        ]
        read_only_fields = ['asset_id', 'barcode', 'created_at', 'updated_at', 'logs']


class AssetCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating assets"""
    class Meta:
        model = Asset
        fields = [
            'name', 'description', 'serial_number', 'category',
            'location', 'assigned_to', 'status'
        ]
