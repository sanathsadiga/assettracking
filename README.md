# Asset Tracking System

A complete internal asset tracking system with barcode scanning, printing, and automatic logging.

## 🎯 Features

✅ **Asset Management**
- Automatically generate unique Asset IDs (ASSET0001, ASSET0002, etc.)
- Track asset details (name, category, location, serial number)
- Categorize assets and organize by location

✅ **Barcode System**
- Generate Code128 barcodes for each asset
- Print single or multiple barcodes per A4 PDF
- Barcode = Asset ID (same value)

✅ **Scanning**
- Scan using mobile camera (html5-qrcode)
- USB barcode scanner support
- Instant asset information display

✅ **Asset Status Tracking**
- Available
- In Use
- Under Repair
- Retired

✅ **Assignment Management**
- Assign assets to users
- Track asset ownership
- Update status and location

✅ **Comprehensive Logging**
- Log every action (created, assigned, scanned, updated)
- Track who performed each action and when
- View full audit trail per asset

✅ **Role-Based Access**
- Admin: Create assets, print barcodes, view all data
- Users: Scan, view assigned assets, update status

## 🛠️ Tech Stack

**Backend**
- Django 4.2
- Django REST Framework 3.14
- MySQL 8.0
- Python 3.8+

**Frontend**
- Django Templates
- Bootstrap 5
- HTML5 QR Code Scanner
- ReportLab (PDF generation)
- python-barcode (barcode generation)

**Libraries**
- reportlab - PDF generation
- python-barcode - Barcode generation
- Pillow - Image processing
- django-cors-headers - CORS support
- python-decouple - Environment configuration

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server running
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone/Extract Project

```bash
cd /path/to/asset-tracking-system
```

### 2. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=asset_tracking
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Create Database

```bash
# In MySQL
CREATE DATABASE asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (enter password)
```

### 8. Create Initial Data (Optional)

```bash
python manage.py shell
```

```python
from tracker.models import Category, Location

# Create categories
Category.objects.create(name='Laptop', description='Laptop computers')
Category.objects.create(name='Desktop', description='Desktop computers')
Category.objects.create(name='Monitor', description='Computer monitors')
Category.objects.create(name='Printer', description='Printers')
Category.objects.create(name='Phone', description='Mobile phones')

# Create locations
Location.objects.create(name='Bangalore', description='Bangalore Office')
Location.objects.create(name='Mumbai', description='Mumbai Office')
Location.objects.create(name='Delhi', description='Delhi Office')

exit()
```

### 9. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 10. Run Development Server

```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000`

## 🚀 Usage

### Login
- URL: `http://localhost:8000/login/`
- Admin credentials: Use the superuser you created

### Dashboard
- View asset statistics
- See recent activity
- Quick access to main features

### Add Assets (Admin Only)
1. Go to "Add Asset" page
2. Fill asset details:
   - Name (required)
   - Serial Number (optional)
   - Category (required)
   - Location (required)
   - Description (optional)
3. Click "Create Asset"
4. System auto-generates Asset ID and Barcode

### Print Barcodes
1. Go to Asset Details page
2. Click "Print Barcode" button
3. Choose format (single or multiple)
4. PDF downloads with barcode
5. Print and stick on asset

### Scan Assets
1. Go to "Scan Barcode" page
2. Allow camera access in browser
3. Position barcode in camera view
4. Or use manual entry for USB scanner
5. View asset details immediately
6. Action logged automatically

### Update Status
1. View asset details
2. Click "Edit" button
3. Change status or assignment
4. Save changes
5. Log entry created automatically

### View Logs
1. Go to "Logs" page
2. Filter by asset or action
3. See complete audit trail
4. View who did what and when

## 📁 Project Structure

```
asset-tracking-system/
├── asset_system/              # Django project
│   ├── settings.py           # Project settings
│   ├── urls.py              # Main URL config
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── tracker/                  # Django app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── views_frontend.py    # Template views
│   ├── serializers.py       # DRF serializers
│   ├── admin.py             # Admin interface
│   ├── barcode_utils.py     # Barcode generation
│   ├── urls.py              # App URLs
│   ├── api/
│   │   └── urls.py          # API URLs
│   └── apps.py              # App config
├── templates/               # HTML templates
│   └── tracker/
│       ├── base.html        # Base template
│       ├── login.html       # Login page
│       ├── dashboard.html   # Dashboard
│       ├── asset_list.html  # Asset list
│       ├── asset_detail.html # Asset details
│       ├── add_asset.html   # Add asset form
│       ├── scan.html        # Scan page
│       └── logs.html        # Logs page
├── static/                  # Static files (CSS, JS)
├── media/                   # User uploads (barcodes)
├── logs/                    # Application logs
├── manage.py               # Django management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /admin/` - Django admin login

### Assets
- `GET /api/assets/` - List all assets
- `POST /api/assets/` - Create asset
- `GET /api/assets/{id}/` - Get asset details
- `PUT /api/assets/{id}/` - Update asset
- `POST /api/assets/scan/` - Scan barcode
- `POST /api/assets/{id}/assign/` - Assign to user
- `POST /api/assets/{id}/unassign/` - Unassign from user
- `GET /api/assets/{id}/print_barcode/` - Download barcode PDF
- `POST /api/assets/print_multiple_barcodes/` - Print multiple barcodes
- `GET /api/assets/statistics/` - Get dashboard stats

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category

### Locations
- `GET /api/locations/` - List locations
- `POST /api/locations/` - Create location

### Logs
- `GET /api/logs/` - List all logs
- `GET /api/logs/?asset={id}` - Logs for specific asset

## 🔐 Security Features

✅ CSRF Protection
✅ SQL Injection Prevention (ORM)
✅ XSS Protection (Template escaping)
✅ Session-based authentication
✅ Role-based access control
✅ Audit logging for compliance

## 🐛 Troubleshooting

### Database Connection Error
```
Check MySQL is running:
- macOS: brew services start mysql
- Linux: sudo systemctl start mysql
- Windows: Open Services and start MySQL
```

### Missing Database
```
python manage.py migrate
```

### Static Files Not Loading
```
python manage.py collectstatic --noinput
```

### Permission Denied on Media Files
```
chmod -R 755 media/
```

### Port Already in Use
```
python manage.py runserver 8001
```

## 📊 Database Models

### Asset
- asset_id (unique)
- barcode (unique, same as asset_id)
- name
- description
- serial_number
- category (FK)
- location (FK)
- assigned_to (FK to User)
- status (available, in_use, repair, retired)
- created_by (FK to User)
- created_at, updated_at

### AssetLog
- asset (FK)
- action (created, assigned, scanned, etc.)
- performed_by (FK to User)
- old_value
- new_value
- timestamp
- notes

### Category
- name (unique)
- description

### Location
- name (unique)
- description

## 🔄 Deployment

### Local Network
```bash
# Make server accessible on LAN
python manage.py runserver 0.0.0.0:8000
# Access via: http://<your-ip>:8000
```

### Production (VPS/AWS)
1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS`
3. Use production database
4. Set up HTTPS
5. Use Gunicorn + Nginx
6. Configure firewall rules

Example Gunicorn startup:
```bash
gunicorn asset_system.wsgi:application --bind 0.0.0.0:8000
```

## 📞 Support

For issues, refer to:
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- HTML5 QR Code: https://github.com/mebjas/html5-qrcode

## 📄 License

Internal use only

---

**Made with ❤️ for Asset Management**

Version: 1.0.0
Last Updated: March 2026
