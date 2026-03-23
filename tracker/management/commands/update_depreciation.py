"""
Management command to update asset depreciation values.
Run periodically (daily or weekly) to keep depreciation values current.

Usage:
    python manage.py update_depreciation
    python manage.py update_depreciation --verbose
"""

from django.core.management.base import BaseCommand
from tracker.models import Asset, AssetLog
from decimal import Decimal
from datetime import datetime


class Command(BaseCommand):
    help = 'Update depreciation values for all assets based on their purchase date and depreciation rate'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Print detailed information about each asset updated',
        )

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        
        # Get all assets with financial information
        assets = Asset.objects.filter(
            purchase_cost__isnull=False,
            purchase_date__isnull=False
        )
        
        updated_count = 0
        total_count = assets.count()
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting depreciation update for {total_count} assets...')
        )
        
        for asset in assets:
            try:
                old_value = asset.current_value
                new_value = asset.calculate_depreciation()
                
                # Update the asset if value changed
                if old_value != new_value:
                    asset.current_value = new_value
                    asset.save(update_fields=['current_value', 'updated_at'])
                    updated_count += 1
                    
                    # Log the depreciation update
                    AssetLog.objects.create(
                        asset=asset,
                        action='updated',
                        performed_by=None,  # System action
                        old_value=str(old_value) if old_value else 'N/A',
                        new_value=str(new_value),
                        notes=f'Automatic depreciation update: ₹{old_value} → ₹{new_value}'
                    )
                    
                    if verbose:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ {asset.asset_id} ({asset.name}): '
                                f'₹{old_value} → ₹{new_value}'
                            )
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error updating {asset.asset_id}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Depreciation update complete!\n'
                f'Updated: {updated_count}/{total_count} assets'
            )
        )
