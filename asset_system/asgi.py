"""
ASGI config for asset_system project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asset_system.settings')

application = get_asgi_application()
