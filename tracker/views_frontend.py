"""
Frontend Views for Asset Tracking System
"""
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q
from tracker.models import Asset, AssetLog, Category, Location, Department
from django.contrib.auth.models import User
import json
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from decimal import Decimal


def generate_barcode_svg(barcode_value):
    """Generate SVG barcode from barcode value"""
    try:
        # Use CODE128 format (most compatible)
        barcode_obj = barcode.get('code128', barcode_value, writer=ImageWriter())
        
        # Generate to bytes
        buffer = BytesIO()
        barcode_obj.write(buffer)
        buffer.seek(0)
        
        # Encode to base64 for embedding in HTML
        barcode_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{barcode_base64}"
    except Exception as e:
        return None


class LoginView(DjangoLoginView):
    """Login page"""
    template_name = 'tracker/login.html'
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    """Logout"""
    next_page = 'tracker:login'


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard with statistics"""
    template_name = 'tracker/dashboard.html'
    login_url = 'tracker:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get assets based on user role
        if user.is_staff:
            assets = Asset.objects.all()
        else:
            assets = Asset.objects.filter(
                Q(assigned_to=user) | Q(status='available')
            )
        
        # Statistics
        context['total_assets'] = assets.count()
        context['available_assets'] = assets.filter(status='available').count()
        context['in_use_assets'] = assets.filter(status='in_use').count()
        context['repair_assets'] = assets.filter(status='repair').count()
        
        # Financial totals
        total_purchase_cost = sum(
            Decimal(str(asset.purchase_cost)) for asset in assets if asset.purchase_cost
        ) if assets else Decimal('0')
        total_current_value = sum(
            Decimal(str(asset.current_value)) if asset.current_value else Decimal('0') 
            for asset in assets
        ) if assets else Decimal('0')
        total_depreciation = total_purchase_cost - total_current_value
        
        context['total_purchase_cost'] = total_purchase_cost
        context['total_current_value'] = total_current_value
        context['total_depreciation'] = total_depreciation
        
        # Recent logs
        context['recent_logs'] = AssetLog.objects.select_related(
            'asset', 'performed_by'
        ).order_by('-timestamp')[:10]
        
        context['is_admin'] = user.is_staff
        
        return context


class AssetListView(LoginRequiredMixin, ListView):
    """Asset list with search and filter"""
    template_name = 'tracker/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 20
    login_url = 'tracker:login'

    def get_queryset(self):
        user = self.request.user
        
        # Get assets based on user role
        if user.is_staff:
            assets = Asset.objects.select_related('category', 'location', 'department', 'assigned_to')
        else:
            assets = Asset.objects.filter(
                Q(assigned_to=user) | Q(status='available')
            ).select_related('category', 'location', 'department', 'assigned_to')
        
        # Search
        search_query = self.request.GET.get('q')
        if search_query:
            assets = assets.filter(
                Q(asset_id__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(barcode__icontains=search_query) |
                Q(serial_number__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status')
        if status_filter:
            assets = assets.filter(status=status_filter)
        
        # Filter by category
        category_filter = self.request.GET.get('category')
        if category_filter:
            assets = assets.filter(category_id=category_filter)
        
        # Filter by location
        location_filter = self.request.GET.get('location')
        if location_filter:
            assets = assets.filter(location_id=location_filter)
        
        # Advanced Laptop/Desktop Filters
        cpu_make = self.request.GET.get('cpu_make')
        if cpu_make:
            assets = assets.filter(cpu_make__icontains=cpu_make)
        
        model = self.request.GET.get('model')
        if model:
            assets = assets.filter(model__icontains=model)
        
        processor = self.request.GET.get('processor')
        if processor:
            assets = assets.filter(processor__icontains=processor)
        
        ram = self.request.GET.get('ram')
        if ram:
            assets = assets.filter(ram__icontains=ram)
        
        hdd = self.request.GET.get('hdd')
        if hdd:
            assets = assets.filter(hdd__icontains=hdd)
        
        os_filter = self.request.GET.get('os')
        if os_filter:
            assets = assets.filter(os__icontains=os_filter)
        
        ms_office = self.request.GET.get('ms_office')
        if ms_office:
            assets = assets.filter(ms_office_version__icontains=ms_office)
        
        antivirus = self.request.GET.get('antivirus')
        if antivirus:
            assets = assets.filter(antivirus=antivirus)
        
        ip_address = self.request.GET.get('ip_address')
        if ip_address:
            assets = assets.filter(ip_address__icontains=ip_address)
        
        hostname = self.request.GET.get('hostname')
        if hostname:
            assets = assets.filter(hostname__icontains=hostname)
        
        username = self.request.GET.get('username')
        if username:
            assets = assets.filter(username__icontains=username)
        
        # Boolean filters for software
        e1_user = self.request.GET.get('e1_user')
        if e1_user == 'true':
            assets = assets.filter(e1_user=True)
        elif e1_user == 'false':
            assets = assets.filter(e1_user=False)
        
        e3_user = self.request.GET.get('e3_user')
        if e3_user == 'true':
            assets = assets.filter(e3_user=True)
        elif e3_user == 'false':
            assets = assets.filter(e3_user=False)
        
        srilipi = self.request.GET.get('srilipi')
        if srilipi == 'true':
            assets = assets.filter(srilipi=True)
        elif srilipi == 'false':
            assets = assets.filter(srilipi=False)
        
        photoshop = self.request.GET.get('photoshop')
        if photoshop == 'true':
            assets = assets.filter(photoshop=True)
        elif photoshop == 'false':
            assets = assets.filter(photoshop=False)
        
        indesign = self.request.GET.get('indesign')
        if indesign == 'true':
            assets = assets.filter(indesign=True)
        elif indesign == 'false':
            assets = assets.filter(indesign=False)
        
        illustrator = self.request.GET.get('illustrator')
        if illustrator == 'true':
            assets = assets.filter(illustrator=True)
        elif illustrator == 'false':
            assets = assets.filter(illustrator=False)
        
        corel_draw = self.request.GET.get('corel_draw')
        if corel_draw == 'true':
            assets = assets.filter(corel_draw=True)
        elif corel_draw == 'false':
            assets = assets.filter(corel_draw=False)
        
        distiller = self.request.GET.get('distiller')
        if distiller == 'true':
            assets = assets.filter(distiller=True)
        elif distiller == 'false':
            assets = assets.filter(distiller=False)
        
        newswrap = self.request.GET.get('newswrap')
        if newswrap == 'true':
            assets = assets.filter(newswrap=True)
        elif newswrap == 'false':
            assets = assets.filter(newswrap=False)
        
        idm_role = self.request.GET.get('idm_role')
        if idm_role:
            assets = assets.filter(idm_role__icontains=idm_role)
        
        email = self.request.GET.get('email')
        if email:
            assets = assets.filter(official_email__icontains=email)
        
        sap_id = self.request.GET.get('sap_id')
        if sap_id:
            assets = assets.filter(sap_id__icontains=sap_id)
        
        finance_code = self.request.GET.get('finance_code')
        if finance_code:
            assets = assets.filter(finance_asset_code__icontains=finance_code)
        
        po_number = self.request.GET.get('po_number')
        if po_number:
            assets = assets.filter(po_number__icontains=po_number)
        
        invoice_number = self.request.GET.get('invoice_number')
        if invoice_number:
            assets = assets.filter(invoice_number__icontains=invoice_number)
        
        serial_number_filter = self.request.GET.get('serial_number_filter')
        if serial_number_filter:
            assets = assets.filter(serial_number__icontains=serial_number_filter)
        
        return assets.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['locations'] = Location.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['is_admin'] = self.request.user.is_staff
        context['unique_os_list'] = Asset.get_unique_os_list()
        context['unique_ms_office_list'] = Asset.get_unique_ms_office_list()
        context['unique_processor_list'] = Asset.get_unique_processor_list()
        return context


class AssetDetailView(LoginRequiredMixin, DetailView):
    """Asset detail with logs"""
    model = Asset
    template_name = 'tracker/asset_detail.html'
    context_object_name = 'asset'
    login_url = 'tracker:login'

    def get_queryset(self):
        """Optimize query with select_related"""
        return Asset.objects.select_related('assigned_to', 'category', 'location', 'department', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = self.get_object()
        context['logs'] = asset.logs.select_related('performed_by').order_by('-timestamp')
        context['is_admin'] = self.request.user.is_staff
        context['assigned_users'] = User.objects.filter(is_active=True)
        context['locations'] = Location.objects.all()
        context['departments'] = Department.objects.all()
        return context


class AddAssetView(LoginRequiredMixin, TemplateView):
    """Add new asset (Admin only)"""
    template_name = 'tracker/add_asset.html'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['locations'] = Location.objects.all()
        context['users'] = User.objects.filter(is_active=True)
        context['unique_os_list'] = Asset.get_unique_os_list()
        context['unique_ms_office_list'] = Asset.get_unique_ms_office_list()
        context['unique_processor_list'] = Asset.get_unique_processor_list()
        return context

    def post(self, request, *args, **kwargs):
        try:
            from datetime import datetime
            from decimal import Decimal
            
            # Validate required fields
            purchase_date_str = request.POST.get('purchase_date', '').strip()
            purchase_cost_str = request.POST.get('purchase_cost', '').strip()
            
            if not purchase_date_str:
                raise ValueError("Purchase Date is required")
            if not purchase_cost_str:
                raise ValueError("Purchase Cost is required")
            
            # Check asset_id generation method
            auto_generate_asset_id = request.POST.get('auto_generate_asset_id') == 'on'
            manual_asset_id = request.POST.get('asset_id', '').strip() if not auto_generate_asset_id else None
            
            # If manual, validate that asset_id is provided
            if not auto_generate_asset_id and not manual_asset_id:
                raise ValueError("Asset ID is required when not auto-generating")
            
            # Check if manual asset_id already exists
            if manual_asset_id and Asset.objects.filter(asset_id=manual_asset_id).exists():
                raise ValueError(f"Asset ID '{manual_asset_id}' already exists")
            
            # Get financial data
            depreciation_rate_str = request.POST.get('depreciation_rate')
            
            purchase_date = None
            purchase_cost = None
            depreciation_rate = 0
            
            # Parse dates and numbers
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
            purchase_cost = Decimal(purchase_cost_str)
            if depreciation_rate_str:
                depreciation_rate = Decimal(depreciation_rate_str)
            
            # Prepare asset creation data
            asset_data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'serial_number': request.POST.get('serial_number'),
                'category_id': request.POST.get('category'),
                'location_id': request.POST.get('location'),
                'department_id': request.POST.get('department'),
                'purchase_date': purchase_date,
                'purchase_cost': purchase_cost,
                'depreciation_rate': depreciation_rate,
                'created_by': request.user,
                'asset_id_auto_generated': auto_generate_asset_id,
            }
            
            # Add manual asset_id if provided
            if manual_asset_id:
                asset_data['asset_id'] = manual_asset_id
                asset_data['barcode'] = manual_asset_id
            
            # Add laptop/desktop specific fields if category is Laptop or Desktop
            category_id = request.POST.get('category')
            if category_id:
                category = Category.objects.get(id=category_id)
                if category.name.lower() in ['laptop', 'desktop', 'pc']:
                    asset_data['cpu_make'] = request.POST.get('cpu_make')
                    asset_data['model'] = request.POST.get('model')
                    asset_data['processor'] = request.POST.get('processor')
                    asset_data['ram'] = request.POST.get('ram')
                    asset_data['hdd'] = request.POST.get('hdd')
                    asset_data['os'] = request.POST.get('os')
                    asset_data['ms_office_version'] = request.POST.get('ms_office_version')
                    asset_data['ip_address'] = request.POST.get('ip_address')
                    asset_data['hostname'] = request.POST.get('hostname')
                    asset_data['e1_user'] = request.POST.get('e1_user') == 'on'
                    asset_data['e3_user'] = request.POST.get('e3_user') == 'on'
                    asset_data['antivirus'] = request.POST.get('antivirus', 'no')
                    asset_data['srilipi'] = request.POST.get('srilipi') == 'on'
                    asset_data['photoshop'] = request.POST.get('photoshop') == 'on'
                    asset_data['indesign'] = request.POST.get('indesign') == 'on'
                    asset_data['illustrator'] = request.POST.get('illustrator') == 'on'
                    asset_data['corel_draw'] = request.POST.get('corel_draw') == 'on'
                    asset_data['distiller'] = request.POST.get('distiller') == 'on'
                    asset_data['newswrap'] = request.POST.get('newswrap') == 'on'
                    asset_data['idm_role'] = request.POST.get('idm_role')
                    asset_data['username'] = request.POST.get('username')
                    asset_data['official_email'] = request.POST.get('official_email')
                    asset_data['sap_id'] = request.POST.get('sap_id')
                    asset_data['installation_date'] = request.POST.get('installation_date') or None
                    asset_data['warranty_expiry_date'] = request.POST.get('warranty_expiry_date') or None
                    asset_data['po_number'] = request.POST.get('po_number')
                    asset_data['invoice_number'] = request.POST.get('invoice_number')
                    asset_data['finance_asset_code'] = request.POST.get('finance_asset_code')
            
            # Add common fields
            asset_data['status'] = request.POST.get('status', 'available')
            asset_data['remarks'] = request.POST.get('remarks')
            
            asset = Asset.objects.create(**asset_data)
            
            # Log creation
            financial_info = ""
            if purchase_cost:
                financial_info = f"Cost: ₹{purchase_cost}, Depreciation: {depreciation_rate}%"
            
            AssetLog.objects.create(
                asset=asset,
                action='created',
                performed_by=request.user,
                new_value=asset.name,
                notes=financial_info if financial_info else None
            )
            
            return redirect('tracker:asset_detail', pk=asset.pk)
        except Exception as e:
            context = self.get_context_data()
            context['error'] = str(e)
            return render(request, self.template_name, context)


class ScanView(LoginRequiredMixin, TemplateView):
    """Scan page with camera"""
    template_name = 'tracker/scan.html'
    login_url = 'tracker:login'


class ScanResultView(LoginRequiredMixin, View):
    """Process scan result (AJAX)"""
    login_url = 'tracker:login'

    def post(self, request):
        try:
            data = json.loads(request.body)
            barcode = data.get('barcode')
            
            if not barcode:
                return JsonResponse({
                    'success': False,
                    'message': 'Barcode is required'
                })
            
            # Find asset
            try:
                asset = Asset.objects.get(barcode=barcode)
            except Asset.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Asset with barcode {barcode} not found'
                })
            
            # Log scan
            AssetLog.objects.create(
                asset=asset,
                action='scanned',
                performed_by=request.user,
                notes=f"Scanned via web camera"
            )
            
            return JsonResponse({
                'success': True,
                'asset': {
                    'id': asset.id,
                    'asset_id': asset.asset_id,
                    'barcode': asset.barcode,
                    'name': asset.name,
                    'category': asset.category.name if asset.category else 'N/A',
                    'location': asset.location.name if asset.location else 'N/A',
                    'status': asset.get_status_display(),
                    'assigned_to': asset.assigned_to.get_full_name() if asset.assigned_to else 'Unassigned',
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })


class UpdateAssetStatusView(LoginRequiredMixin, View):
    """Update asset status, location, and assignment (Admin or assigned user)"""
    login_url = 'tracker:login'

    def post(self, request, pk):
        asset = get_object_or_404(Asset, pk=pk)
        
        # Check permission
        if not request.user.is_staff and asset.assigned_to != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You do not have permission to update this asset'
            }, status=403)
        
        try:
            # Store old values for logging
            old_status = asset.status
            old_assigned = asset.assigned_to
            old_location = asset.location
            old_department = asset.department
            
            # Update status
            status = request.POST.get('status')
            if status and status != '':
                asset.status = status
            
            # Update location
            location_id = request.POST.get('location')
            if location_id and location_id != '':
                asset.location_id = int(location_id)
            
            # Update department
            department_id = request.POST.get('department')
            if department_id and department_id != '':
                asset.department_id = int(department_id)
            
            # Update assignment
            assigned_to_id = request.POST.get('assigned_to')
            if assigned_to_id and assigned_to_id != '':
                asset.assigned_to_id = int(assigned_to_id)
            elif request.POST.get('assigned_to') == '':
                # Empty string means unassign
                asset.assigned_to = None
            
            asset.save()
            
            # Log status changes
            if status and status != '' and old_status != asset.status:
                AssetLog.objects.create(
                    asset=asset,
                    action='status_changed',
                    performed_by=request.user,
                    old_value=old_status,
                    new_value=asset.status
                )
            
            # Log assignment changes
            if old_assigned != asset.assigned_to:
                AssetLog.objects.create(
                    asset=asset,
                    action='assigned',
                    performed_by=request.user,
                    old_value=str(old_assigned) if old_assigned else 'Unassigned',
                    new_value=str(asset.assigned_to) if asset.assigned_to else 'Unassigned'
                )
            
            # Log location changes
            if location_id and location_id != '' and old_location != asset.location:
                AssetLog.objects.create(
                    asset=asset,
                    action='location_changed',
                    performed_by=request.user,
                    old_value=str(old_location) if old_location else 'No location',
                    new_value=str(asset.location) if asset.location else 'No location'
                )
            
            # Log department changes
            if department_id and department_id != '' and old_department != asset.department:
                AssetLog.objects.create(
                    asset=asset,
                    action='department_changed',
                    performed_by=request.user,
                    old_value=str(old_department) if old_department else 'No department',
                    new_value=str(asset.department) if asset.department else 'No department'
                )
            
            return redirect('tracker:asset_detail', pk=asset.pk)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class LogsView(LoginRequiredMixin, ListView):
    """View asset logs"""
    template_name = 'tracker/logs.html'
    context_object_name = 'logs'
    paginate_by = 50
    login_url = 'tracker:login'

    def get_queryset(self):
        user = self.request.user
        
        # Get logs based on user role
        if user.is_staff:
            logs = AssetLog.objects.select_related('asset', 'performed_by')
        else:
            # Regular users see logs only for their assigned assets
            logs = AssetLog.objects.filter(
                asset__assigned_to=user
            ).select_related('asset', 'performed_by')
        
        # Filter by asset
        asset_id = self.request.GET.get('asset_id')
        if asset_id:
            logs = logs.filter(asset__asset_id=asset_id)
        
        # Filter by action
        action = self.request.GET.get('action')
        if action:
            logs = logs.filter(action=action)
        
        return logs.order_by('-timestamp')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_staff:
            context['assets'] = Asset.objects.all()
        else:
            context['assets'] = Asset.objects.filter(assigned_to=user)
        
        context['is_admin'] = user.is_staff
        return context


class TestLibraryView(TemplateView):
    """Test if Html5Qrcode library loads correctly"""
    template_name = 'tracker/test_library.html'


# ============================================================================
# MANAGEMENT VIEWS (ADMIN ONLY)
# ============================================================================

class ManageLocationsView(LoginRequiredMixin, ListView):
    """Manage locations (Admin only)"""
    template_name = 'tracker/manage_locations.html'
    context_object_name = 'locations'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Location.objects.all().order_by('name')


class AddLocationView(LoginRequiredMixin, View):
    """Add new location (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                return redirect('tracker:manage_locations')

            Location.objects.create(name=name, description=description if description else None)
            return redirect('tracker:manage_locations')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EditLocationView(LoginRequiredMixin, View):
    """Edit location (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            location_id = request.POST.get('id')
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            location = get_object_or_404(Location, id=location_id)
            location.name = name
            location.description = description if description else None
            location.save()

            return redirect('tracker:manage_locations')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class DeleteLocationView(LoginRequiredMixin, View):
    """Delete location (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, location_id):
        try:
            location = get_object_or_404(Location, id=location_id)
            location.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class ManageDepartmentsView(LoginRequiredMixin, ListView):
    """Manage departments (Admin only)"""
    template_name = 'tracker/manage_departments.html'
    context_object_name = 'departments'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Department.objects.all().order_by('name')


class AddDepartmentView(LoginRequiredMixin, View):
    """Add new department (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                return redirect('tracker:manage_departments')

            Department.objects.create(name=name, description=description if description else None)
            return redirect('tracker:manage_departments')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EditDepartmentView(LoginRequiredMixin, View):
    """Edit department (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            department_id = request.POST.get('id')
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            department = get_object_or_404(Department, id=department_id)
            department.name = name
            department.description = description if description else None
            department.save()

            return redirect('tracker:manage_departments')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class DeleteDepartmentView(LoginRequiredMixin, View):
    """Delete department (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, department_id):
        try:
            department = get_object_or_404(Department, id=department_id)
            department.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class ManageUsersView(LoginRequiredMixin, ListView):
    """Manage users (Admin only)"""
    template_name = 'tracker/manage_users.html'
    context_object_name = 'users'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.all().order_by('username')


class AddUserView(LoginRequiredMixin, View):
    """Add new user (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            is_staff = request.POST.get('is_staff') == 'on'

            if not username or not email or not password:
                return redirect('tracker:manage_users')

            if password != password2:
                return redirect('tracker:manage_users')

            if User.objects.filter(username=username).exists():
                return redirect('tracker:manage_users')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=True
            )
            return redirect('tracker:manage_users')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EditUserView(LoginRequiredMixin, View):
    """Edit user (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            user_id = request.POST.get('id')
            email = request.POST.get('email', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            password = request.POST.get('password', '').strip()
            is_staff = request.POST.get('is_staff') == 'on'
            is_active = request.POST.get('is_active') == 'on'

            user = get_object_or_404(User, id=user_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_active = is_active

            if password:
                user.set_password(password)

            user.save()
            return redirect('tracker:manage_users')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class DeleteUserView(LoginRequiredMixin, View):
    """Delete user (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            if user.is_superuser:
                return JsonResponse({'success': False, 'message': 'Cannot delete superuser'}, status=400)
            user.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class ManageCategoriesView(LoginRequiredMixin, ListView):
    """Manage categories (Admin only)"""
    template_name = 'tracker/manage_categories.html'
    context_object_name = 'categories'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.all().order_by('name')


class AddCategoryView(LoginRequiredMixin, View):
    """Add new category (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                return redirect('tracker:manage_categories')

            if Category.objects.filter(name=name).exists():
                return redirect('tracker:manage_categories')

            Category.objects.create(
                name=name,
                description=description if description else None
            )
            return redirect('tracker:manage_categories')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EditCategoryView(LoginRequiredMixin, View):
    """Edit category (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            category_id = request.POST.get('id')
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            category = get_object_or_404(Category, id=category_id)
            category.name = name
            category.description = description if description else None
            category.save()
            return redirect('tracker:manage_categories')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class DeleteCategoryView(LoginRequiredMixin, View):
    """Delete category (Admin only)"""
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, category_id):
        try:
            category = get_object_or_404(Category, id=category_id)
            # Check if category has assets
            if category.assets.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Cannot delete category with existing assets'
                }, status=400)
            category.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class BulkAddAssetView(LoginRequiredMixin, TemplateView):
    """Add multiple assets at once (Admin only)"""
    template_name = 'tracker/bulk_add_asset.html'
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['locations'] = Location.objects.all()
        context['users'] = User.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        try:
            from datetime import datetime
            from decimal import Decimal
            
            # Get form data
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            quantity = request.POST.get('quantity', '1').strip()
            category_id = request.POST.get('category')
            location_id = request.POST.get('location')
            
            # Get financial data (required)
            purchase_date_str = request.POST.get('purchase_date', '').strip()
            purchase_cost_str = request.POST.get('purchase_cost', '').strip()
            depreciation_rate_str = request.POST.get('depreciation_rate', '0')
            
            # Validation
            if not name:
                raise ValueError("Asset name is required")
            if not quantity or not quantity.isdigit() or int(quantity) < 1:
                raise ValueError("Quantity must be a positive number")
            if int(quantity) > 500:
                raise ValueError("Maximum quantity is 500 items at once")
            if not purchase_date_str:
                raise ValueError("Purchase Date is required")
            if not purchase_cost_str:
                raise ValueError("Purchase Cost is required")
            
            quantity = int(quantity)
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
            purchase_cost = Decimal(purchase_cost_str)
            depreciation_rate = Decimal(depreciation_rate_str) if depreciation_rate_str else Decimal('0')
            
            # Create assets
            created_assets = []
            errors = []
            
            for i in range(quantity):
                try:
                    # Generate unique asset name with suffix if quantity > 1
                    asset_name = name
                    if quantity > 1:
                        asset_name = f"{name} #{i+1}"
                    
                    asset = Asset.objects.create(
                        name=asset_name,
                        description=description if description else None,
                        category_id=category_id,
                        location_id=location_id,
                        purchase_date=purchase_date,
                        purchase_cost=purchase_cost,
                        depreciation_rate=depreciation_rate,
                        created_by=request.user
                    )
                    
                    # Log creation
                    financial_info = f"Cost: ₹{purchase_cost}, Depreciation: {depreciation_rate}%"
                    AssetLog.objects.create(
                        asset=asset,
                        action='created',
                        performed_by=request.user,
                        new_value=asset_name,
                        notes=financial_info
                    )
                    
                    created_assets.append(asset)
                except Exception as e:
                    errors.append(f"Item #{i+1}: {str(e)}")
            
            # If we created at least one asset, show success
            if created_assets:
                context = self.get_context_data()
                context['success_message'] = f"Successfully created {len(created_assets)} asset(s)"
                context['created_assets'] = created_assets
                context['errors'] = errors if errors else None
                
                # If creating for printing barcodes
                if request.POST.get('print_barcodes'):
                    return render(request, 'tracker/barcode_print.html', {
                        'assets': created_assets,
                        'is_bulk': True
                    })
                
                return render(request, self.template_name, context)
            else:
                raise ValueError(f"Failed to create assets: {'; '.join(errors)}")
        except Exception as e:
            context = self.get_context_data()
            context['error'] = str(e)
            return render(request, self.template_name, context)


class BarcodePrintView(LoginRequiredMixin, View):
    """Print barcodes for assets"""
    template_name = 'tracker/barcode_print_simple.html'  # Use simple print-focused template
    login_url = 'tracker:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tracker:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_assets(self, request):
        """Get asset IDs from query params or POST"""
        asset_ids = request.GET.getlist('asset_ids')
        if not asset_ids and request.method == 'POST':
            asset_ids = request.POST.getlist('asset_ids')
        
        # Convert to integers for safety
        asset_ids = [int(aid) for aid in asset_ids if aid.isdigit()]
        
        if asset_ids:
            # Use select_related to optimize query for large datasets
            return Asset.objects.filter(id__in=asset_ids).select_related('category', 'location').order_by('asset_id')
        return []

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""
        try:
            assets = list(self.get_assets(request))
            # Add barcode image to each asset
            for asset in assets:
                asset.barcode_image = generate_barcode_svg(asset.barcode)
            
            # Calculate financial totals
            total_purchase_cost = sum(Decimal(str(asset.purchase_cost)) for asset in assets if asset.purchase_cost)
            total_current_value = sum(Decimal(str(asset.current_value)) if asset.current_value else Decimal('0') for asset in assets)
            total_depreciation = total_purchase_cost - total_current_value
            
            context = {
                'assets': assets,
                'is_bulk': request.GET.get('bulk') or request.POST.get('is_bulk'),
                'error': None,
                'total_purchase_cost': total_purchase_cost,
                'total_current_value': total_current_value,
                'total_depreciation': total_depreciation,
            }
        except Exception as e:
            context = {
                'assets': [],
                'is_bulk': False,
                'error': f"Error loading assets: {str(e)}",
                'total_purchase_cost': Decimal('0'),
                'total_current_value': Decimal('0'),
                'total_depreciation': Decimal('0'),
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle POST requests from bulk add form"""
        try:
            assets = list(self.get_assets(request))
            # Add barcode image to each asset
            for asset in assets:
                asset.barcode_image = generate_barcode_svg(asset.barcode)
            
            # Calculate financial totals
            total_purchase_cost = sum(Decimal(str(asset.purchase_cost)) for asset in assets if asset.purchase_cost)
            total_current_value = sum(Decimal(str(asset.current_value)) if asset.current_value else Decimal('0') for asset in assets)
            total_depreciation = total_purchase_cost - total_current_value
            
            context = {
                'assets': assets,
                'is_bulk': request.POST.get('is_bulk') or True,
                'error': None,
                'total_purchase_cost': total_purchase_cost,
                'total_current_value': total_current_value,
                'total_depreciation': total_depreciation,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            context = {
                'assets': [],
                'is_bulk': False,
                'error': f"Error loading assets: {str(e)}",
                'total_purchase_cost': Decimal('0'),
                'total_current_value': Decimal('0'),
                'total_depreciation': Decimal('0'),
            }
            return render(request, self.template_name, context)

