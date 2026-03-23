"""
Asset Tracking System - Frontend URL Configuration
"""
from django.urls import path
from tracker.views_frontend import (
    LoginView, LogoutView, DashboardView, AssetListView, AssetDetailView,
    AddAssetView, BulkAddAssetView, BarcodePrintView, ScanView, ScanResultView, UpdateAssetStatusView, LogsView,
    TestLibraryView,
    ManageLocationsView, AddLocationView, EditLocationView, DeleteLocationView,
    ManageDepartmentsView, AddDepartmentView, EditDepartmentView, DeleteDepartmentView,
    ManageUsersView, AddUserView, EditUserView, DeleteUserView,
    ManageCategoriesView, AddCategoryView, EditCategoryView, DeleteCategoryView
)

app_name = 'tracker'

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Asset Management
    path('assets/', AssetListView.as_view(), name='asset_list'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset_detail'),
    path('assets/add/', AddAssetView.as_view(), name='add_asset'),
    path('assets/bulk-add/', BulkAddAssetView.as_view(), name='bulk_add_asset'),
    path('assets/barcode-print/', BarcodePrintView.as_view(), name='barcode_print'),
    
    # Scanning
    path('scan/', ScanView.as_view(), name='scan'),
    path('scan/result/', ScanResultView.as_view(), name='scan_result'),
    path('test-library/', TestLibraryView.as_view(), name='test_library'),
    
    # Updates
    path('assets/<int:pk>/update/', UpdateAssetStatusView.as_view(), name='update_asset'),
    
    # Logs
    path('logs/', LogsView.as_view(), name='logs'),
    
    # Management - Locations
    path('manage/locations/', ManageLocationsView.as_view(), name='manage_locations'),
    path('manage/locations/add/', AddLocationView.as_view(), name='add_location'),
    path('manage/locations/edit/', EditLocationView.as_view(), name='edit_location'),
    path('delete-location/<int:location_id>/', DeleteLocationView.as_view(), name='delete_location'),
    
    # Management - Departments
    path('manage/departments/', ManageDepartmentsView.as_view(), name='manage_departments'),
    path('manage/departments/add/', AddDepartmentView.as_view(), name='add_department'),
    path('manage/departments/edit/', EditDepartmentView.as_view(), name='edit_department'),
    path('delete-department/<int:department_id>/', DeleteDepartmentView.as_view(), name='delete_department'),
    
    # Management - Categories
    path('manage/categories/', ManageCategoriesView.as_view(), name='manage_categories'),
    path('manage/categories/add/', AddCategoryView.as_view(), name='add_category'),
    path('manage/categories/edit/', EditCategoryView.as_view(), name='edit_category'),
    path('manage/categories/<int:category_id>/delete/', DeleteCategoryView.as_view(), name='delete_category'),
    
    # Management - Users
    path('manage/users/', ManageUsersView.as_view(), name='manage_users'),
    path('manage/users/add/', AddUserView.as_view(), name='add_user'),
    path('manage/users/edit/', EditUserView.as_view(), name='edit_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
]
