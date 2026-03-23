"""
API Views for Asset Tracking System
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import FileResponse
from tracker.models import Asset, Category, Location, AssetLog
from tracker.serializers import (
    AssetListSerializer, AssetDetailSerializer, AssetCreateUpdateSerializer,
    CategorySerializer, LocationSerializer, AssetLogSerializer
)
from tracker.barcode_utils import generate_single_barcode_pdf, generate_multiple_barcodes_pdf
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category management"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for Location management"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class AssetViewSet(viewsets.ModelViewSet):
    """ViewSet for Asset management"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'location', 'assigned_to']
    search_fields = ['asset_id', 'barcode', 'name', 'serial_number']
    ordering_fields = ['created_at', 'asset_id', 'name', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Get assets based on user role"""
        user = self.request.user
        if user.is_staff:
            # Admin sees all assets
            return Asset.objects.select_related(
                'category', 'location', 'assigned_to', 'created_by'
            ).prefetch_related('logs')
        else:
            # Regular users see assigned assets
            return Asset.objects.filter(
                Q(assigned_to=user) | Q(status='available')
            ).select_related('category', 'location', 'assigned_to', 'created_by')

    def get_serializer_class(self):
        """Choose serializer based on action"""
        if self.action == 'retrieve':
            return AssetDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AssetCreateUpdateSerializer
        return AssetListSerializer

    def create(self, request, *args, **kwargs):
        """Create new asset"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        asset = serializer.save(created_by=request.user)
        
        # Log asset creation
        AssetLog.objects.create(
            asset=asset,
            action='created',
            performed_by=request.user,
            new_value=asset.name
        )
        
        # Return created asset detail
        output_serializer = AssetDetailSerializer(asset)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update asset"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Track changes
        changes = {}
        for field in ['name', 'description', 'category', 'location', 'assigned_to', 'status']:
            old_value = getattr(instance, field)
            new_value = request.data.get(field, old_value)
            if old_value != new_value:
                changes[field] = (old_value, new_value)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        asset = serializer.save()
        
        # Log changes
        for field, (old, new) in changes.items():
            action_type = 'status_changed' if field == 'status' else 'updated'
            if field == 'assigned_to':
                action_type = 'assigned' if new else 'unassigned'
            
            AssetLog.objects.create(
                asset=asset,
                action=action_type,
                performed_by=request.user,
                old_value=str(old),
                new_value=str(new)
            )
        
        output_serializer = AssetDetailSerializer(asset)
        return Response(output_serializer.data)

    @action(detail=False, methods=['post'])
    def scan(self, request):
        """
        Scan barcode endpoint
        Expected data: {'barcode': 'ASSET0001'}
        """
        barcode = request.data.get('barcode')
        
        if not barcode:
            return Response(
                {'error': 'Barcode is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find asset by barcode
        asset = get_object_or_404(Asset, barcode=barcode)
        
        # Log scan action
        AssetLog.objects.create(
            asset=asset,
            action='scanned',
            performed_by=request.user,
            notes=f"Scanned via {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
        )
        
        # Return asset details
        serializer = AssetDetailSerializer(asset)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign asset to user
        Expected data: {'user_id': 1} or {'user': 1}
        """
        asset = self.get_object()
        user_id = request.data.get('user_id') or request.data.get('user')
        
        if not user_id:
            return Response(
                {'error': 'User ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user
        from django.contrib.auth.models import User
        user = get_object_or_404(User, pk=user_id)
        
        # Update asset
        old_assigned = asset.assigned_to
        asset.assigned_to = user
        asset.status = 'in_use'
        asset.save()
        
        # Log assignment
        AssetLog.objects.create(
            asset=asset,
            action='assigned',
            performed_by=request.user,
            old_value=str(old_assigned) if old_assigned else 'Unassigned',
            new_value=str(user)
        )
        
        serializer = AssetDetailSerializer(asset)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unassign(self, request, pk=None):
        """Unassign asset from user"""
        asset = self.get_object()
        
        old_assigned = asset.assigned_to
        asset.assigned_to = None
        asset.status = 'available'
        asset.save()
        
        # Log unassignment
        AssetLog.objects.create(
            asset=asset,
            action='unassigned',
            performed_by=request.user,
            old_value=str(old_assigned),
            new_value='Unassigned'
        )
        
        serializer = AssetDetailSerializer(asset)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def print_barcode(self, request, pk=None):
        """Generate and download single barcode PDF"""
        asset = self.get_object()
        
        try:
            pdf_bytes = generate_single_barcode_pdf(asset.asset_id, asset.name)
            
            if not pdf_bytes:
                return Response(
                    {'error': 'Failed to generate PDF'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Log print action
            AssetLog.objects.create(
                asset=asset,
                action='updated',
                performed_by=request.user,
                notes='Barcode printed'
            )
            
            return FileResponse(
                io.BytesIO(pdf_bytes),
                as_attachment=True,
                filename=f"{asset.asset_id}_barcode.pdf",
                content_type='application/pdf'
            )
        except Exception as e:
            logger.error(f"Error printing barcode for {asset.asset_id}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def print_multiple_barcodes(self, request):
        """Generate PDF with multiple barcodes"""
        asset_ids = request.data.get('asset_ids', [])
        
        if not asset_ids:
            return Response(
                {'error': 'At least one asset ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get assets
            assets = Asset.objects.filter(asset_id__in=asset_ids)
            
            if not assets.exists():
                return Response(
                    {'error': 'No assets found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Prepare data
            assets_data = [(asset.asset_id, asset.name) for asset in assets]
            
            # Generate PDF
            pdf_bytes = generate_multiple_barcodes_pdf(assets_data)
            
            if not pdf_bytes:
                return Response(
                    {'error': 'Failed to generate PDF'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Log print action for each asset
            for asset in assets:
                AssetLog.objects.create(
                    asset=asset,
                    action='updated',
                    performed_by=request.user,
                    notes='Barcode printed (batch)'
                )
            
            return FileResponse(
                io.BytesIO(pdf_bytes),
                as_attachment=True,
                filename='barcodes.pdf',
                content_type='application/pdf'
            )
        except Exception as e:
            logger.error(f"Error printing multiple barcodes: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get asset statistics for dashboard"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'available': queryset.filter(status='available').count(),
            'in_use': queryset.filter(status='in_use').count(),
            'repair': queryset.filter(status='repair').count(),
            'retired': queryset.filter(status='retired').count(),
            'by_category': {},
            'by_location': {},
        }
        
        # By category
        for category in Category.objects.all():
            stats['by_category'][category.name] = queryset.filter(category=category).count()
        
        # By location
        for location in Location.objects.all():
            stats['by_location'][location.name] = queryset.filter(location=location).count()
        
        return Response(stats)


class AssetLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing asset logs"""
    serializer_class = AssetLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['asset', 'action', 'performed_by']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Get logs based on user role"""
        user = self.request.user
        if user.is_staff:
            return AssetLog.objects.select_related('asset', 'performed_by').all()
        else:
            # Regular users see logs only for their assigned assets
            return AssetLog.objects.filter(
                asset__assigned_to=user
            ).select_related('asset', 'performed_by')


# Import io for file response
import io
