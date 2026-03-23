# Quick Start Guide - Asset Tracking System

## 🚀 Get Running in 5 Minutes

### For macOS/Linux

```bash
# 1. Navigate to project
cd /Users/sanathsadiga/Desktop/asset-tracking-system

# 2. Make script executable
chmod +x run.sh

# 3. Run setup & start server
./run.sh
```

### For Windows

```cmd
# Just double-click or run in CMD:
run.bat
```

---

## ✅ What Gets Automated

The startup script:
1. ✅ Creates Python virtual environment
2. ✅ Installs all dependencies
3. ✅ Creates `.env` file from template
4. ✅ Runs database migrations
5. ✅ Collects static files
6. ✅ Starts Django development server

---

## 🔑 Default Admin Account

After first run, create admin:
```bash
# While in virtual environment:
python manage.py createsuperuser
```

Example:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

---

## 🌐 Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Dashboard |
| `http://localhost:8000/login/` | User Login |
| `http://localhost:8000/admin/` | Admin Panel |
| `http://localhost:8000/api/` | REST API |

---

## 📋 Initial Setup (First Time Only)

### 1. Configure Database (`.env`)

Edit `.env` with MySQL credentials:

```env
DB_NAME=asset_tracking
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 2. Create Categories & Locations

```bash
python manage.py shell
```

```python
from tracker.models import Category, Location

# Categories
Category.objects.create(name='Laptop')
Category.objects.create(name='Desktop')
Category.objects.create(name='Phone')
Category.objects.create(name='Printer')

# Locations
Location.objects.create(name='Bangalore')
Location.objects.create(name='Mumbai')

exit()
```

---

## 🎯 First Time Usage

### 1. Login
- Go to `http://localhost:8000/login/`
- Use admin credentials

### 2. Add Asset
- Click "Add Asset" (Admin only)
- Fill details → System auto-generates Asset ID
- Asset ID format: `ASSET0001`, `ASSET0002`, etc.

### 3. Print Barcode
- Go to asset details
- Click "Print Barcode"
- PDF downloads with barcode
- Print and stick on asset

### 4. Scan Asset
- Go to "Scan Barcode"
- Allow camera permission
- Position barcode in view
- Asset details show instantly

### 5. Update Status
- Click "Edit" on asset
- Change status or assign to user
- Changes logged automatically

---

## 🛠️ Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Run tests
python manage.py test

# Create demo data
python manage.py loaddata demo_data  # (if exists)

# Deactivate virtual environment
deactivate
```

---

## 🔍 File Structure

```
asset-tracking-system/
├── run.sh              # macOS/Linux startup
├── run.bat             # Windows startup
├── manage.py           # Django CLI
├── requirements.txt    # Dependencies
├── README.md          # Full documentation
├── asset_system/       # Django project
│   ├── settings.py    # Configuration
│   ├── urls.py        # Routes
│   └── wsgi.py        # Production server
├── tracker/           # Main app
│   ├── models.py      # Database schema
│   ├── views.py       # API logic
│   ├── views_frontend.py # Template views
│   └── admin.py       # Admin interface
└── templates/         # HTML pages
```

---

## ⚠️ Common Issues

### 1. "Database doesn't exist"
```bash
# Create MySQL database first:
mysql -u root -p
CREATE DATABASE asset_tracking;
```

### 2. "ModuleNotFoundError"
```bash
# Reinstall dependencies:
pip install -r requirements.txt --force-reinstall
```

### 3. "Permission denied" on macOS
```bash
chmod +x run.sh
```

### 4. Port 8000 already in use
```bash
# Use different port:
python manage.py runserver 8001
```

---

## 📊 System Overview

```
Users/Mobile
     ↓
Browser (Chrome, Safari)
     ↓
Django Web Server (localhost:8000)
     ↓
REST API (Barcode scanning)
     ↓
MySQL Database
```

---

## 🎓 Example Workflow

### Admin Setup
1. **Add Asset**: "HP LaserJet Printer" → System generates ASSET0001
2. **Print**: Download barcode PDF
3. **Apply**: Stick barcode on printer

### User Scanning
1. **Open**: http://localhost:8000/scan/
2. **Scan**: Position barcode in camera
3. **View**: Printer details appear instantly
4. **Assign**: Assign printer to "John Doe"
5. **Log**: Action recorded automatically

### Admin Review
1. **Dashboard**: See 1 asset "In Use"
2. **Logs**: View "John Doe assigned printer at 2:30 PM"
3. **Reports**: Track all asset movements

---

## 🚀 Next Steps

- [ ] Start the system (`./run.sh` or `run.bat`)
- [ ] Create admin account
- [ ] Add categories and locations
- [ ] Create first asset
- [ ] Print barcode
- [ ] Test scanning
- [ ] Invite team to use system

---

## 📞 Support

Check `README.md` for:
- Full deployment guide
- API documentation
- Security features
- Database schema
- Troubleshooting

---

**Happy Asset Tracking! 📦**
