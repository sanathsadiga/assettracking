"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.views import (
    AssetViewSet, CategoryViewSet, LocationViewSet, AssetLogViewSet
)

router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'logs', AssetLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]
