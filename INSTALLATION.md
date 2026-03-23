# 📖 Complete Installation & Setup Guide

## 🎯 Overview

This guide will help you set up and run the **Asset Tracking System** from scratch.

---

## ✅ Prerequisites

Before starting, ensure you have:

- **Python 3.8 or higher** 
  - Check: `python --version` or `python3 --version`
- **MySQL Server** (running)
  - Check: `mysql --version`
- **pip** (Python package manager)
  - Check: `pip --version`
- **Git** (optional, for version control)
- **Terminal/Command Prompt** access
- **Text editor** (VS Code, Sublime, etc.)

### For macOS
```bash
# Install Python
brew install python@3.11

# Install MySQL
brew install mysql
brew services start mysql

# Verify installations
python3 --version
mysql --version
```

### For Windows
1. Download Python from python.org
2. Download MySQL from mysql.com
3. Run both installers
4. Add Python to PATH during installation

### For Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip mysql-server

# Start MySQL
sudo systemctl start mysql
```

---

## 🚀 Installation Steps

### Step 1: Navigate to Project

```bash
# macOS/Linux
cd ~/Desktop/asset-tracking-system

# Windows
cd C:\Users\YourUsername\Desktop\asset-tracking-system
```

### Step 2: Create & Activate Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2.8
- Django REST Framework
- MySQL driver
- Barcode generation libraries
- PDF libraries
- And more...

**Installation takes 2-3 minutes.**

### Step 4: Configure Database

#### Create MySQL Database

```bash
# Connect to MySQL
mysql -u root -p

# Enter password when prompted
```

```sql
-- In MySQL console
CREATE DATABASE asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify creation
SHOW DATABASES;
```

Exit MySQL:
```sql
EXIT;
```

#### Configure Environment Variables

Create `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit .env with your database credentials
nano .env  # macOS/Linux
# or use Notepad on Windows
```

**Edit `.env` file:**

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=asset_tracking
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Save and close** the file.

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all database tables.

### Step 6: Create Admin Account (Superuser)

```bash
python manage.py createsuperuser
```

**Example:**
```
Username: admin
Email: admin@example.com
Password: admin123 (or your choice)
Password (again): admin123
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This prepares CSS, JavaScript, and images for serving.

### Step 8: Create Initial Data (Optional)

```bash
python manage.py shell
```

```python
from tracker.models import Category, Location

# Create categories
categories = [
    'Laptop', 'Desktop', 'Monitor', 
    'Printer', 'Phone', 'Tablet'
]
for cat in categories:
    Category.objects.get_or_create(name=cat)

# Create locations
locations = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad']
for loc in locations:
    Location.objects.get_or_create(name=loc)

print("✅ Categories and locations created!")
exit()
```

### Step 9: Run Development Server

```bash
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🌐 Access the System

Open your browser and visit:

| Page | URL |
|------|-----|
| **Dashboard** | http://localhost:8000/ |
| **Admin Panel** | http://localhost:8000/admin/ |
| **Login** | http://localhost:8000/login/ |
| **API** | http://localhost:8000/api/ |

### Login Credentials
- **Username:** admin
- **Password:** (the one you created)

---

## ✨ First Steps After Login

### 1. Add a Category (if not done in shell)
```
Admin Panel → Categories → Add Category
Name: Laptop
Description: Laptop computers
```

### 2. Add a Location
```
Admin Panel → Locations → Add Location
Name: Bangalore
Description: Bangalore Office
```

### 3. Add Your First Asset
```
Dashboard → Add Asset
Name: Dell Laptop
Category: Laptop
Location: Bangalore
Serial Number: SN123456
```

System auto-generates: **ASSET0001**

### 4. Print Barcode
```
Dashboard → Assets → ASSET0001
Button: Print Barcode
Downloads PDF
```

### 5. Test Scanning
```
URL: http://localhost:8000/scan/
1. Click "Start Camera"
2. Show printed barcode to camera
3. Asset details appear
```

---

## 🛠️ Using Automation Scripts

### macOS/Linux

```bash
chmod +x run.sh
./run.sh
```

This script automatically:
1. Creates virtual environment
2. Installs dependencies
3. Runs migrations
4. Starts server

### Windows

```bash
run.bat
```

Double-click `run.bat` in Windows Explorer, or run in Command Prompt.

---

## 🔧 Common Commands

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server on different port
python manage.py runserver 8001

# Check for issues
python manage.py check

# See all available commands
python manage.py help
```

---

## 📊 Database Structure

### What Gets Created

**4 Main Tables:**
1. **tracker_asset** - Assets and their details
2. **tracker_assetlog** - Action logs for each asset
3. **tracker_category** - Asset categories
4. **tracker_location** - Locations/departments

**Django Built-in Tables:**
- auth_user (Users)
- auth_group (Permissions)
- And others...

**Total: ~15 tables**

---

## ⚠️ Troubleshooting

### Issue: "Database connection failed"

**Solution:**
```bash
# Check MySQL is running
mysql -u root -p

# If connection fails, start MySQL
# macOS
brew services start mysql

# Linux
sudo systemctl start mysql

# Windows - check Services app
```

### Issue: "No module named 'django'"

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies again
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Use different port
python manage.py runserver 8001
```

### Issue: "Static files not loading"

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
python manage.py runserver
```

### Issue: "ModuleNotFoundError" after updates

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Permission denied" (macOS/Linux)

**Solution:**
```bash
chmod +x run.sh
chmod -R 755 media/
chmod -R 755 logs/
```

---

## 📁 File Organization

After setup, you'll have:

```
asset-tracking-system/
├── venv/                    # Virtual environment
├── asset_system/            # Django project
├── tracker/                 # Main app
├── templates/               # HTML pages
├── static/                  # CSS, JS, images
├── media/                   # Generated barcodes
├── logs/                    # Application logs
├── db.sqlite3              # (or MySQL connection)
├── manage.py
├── requirements.txt
├── .env                    # Your settings
├── run.sh                  # Startup script
└── README.md
```

---

## 🔐 Security Checklist

For production deployment:

- [ ] Change `DEBUG=False` in `.env`
- [ ] Generate new `SECRET_KEY` in `.env`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Create strong admin password
- [ ] Use environment variables
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Regular database backups
- [ ] Monitor logs

---

## 📈 Performance Optimization

### Database Indexing
Indexes are already created in models.

### Caching (Optional)
Add Redis for caching:
```bash
pip install django-redis
```

### Static Files
Serve via CDN or Nginx in production.

### Database
Use connection pooling in production.

---

## 🚀 Deploy to Production

### Basic Setup (Server/VPS)

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Clone project
git clone your-repo.git

# 3. Install dependencies
cd asset-tracking-system
pip install -r requirements.txt

# 4. Configure .env
nano .env  # Add production settings

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Install Gunicorn
pip install gunicorn

# 8. Start server
gunicorn asset_system.wsgi --bind 0.0.0.0:8000
```

### With Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "asset_system.wsgi", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t asset-tracker .
docker run -p 8000:8000 asset-tracker
```

---

## 🎓 Learning Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Django REST Framework:** https://www.django-rest-framework.org/
- **MySQL Docs:** https://dev.mysql.com/doc/
- **Python Docs:** https://docs.python.org/3/

---

## 💡 Tips & Best Practices

1. **Always use virtual environment**
   - Keep project dependencies isolated

2. **Use .env for secrets**
   - Never commit passwords to git

3. **Regular backups**
   - `mysqldump asset_tracking > backup.sql`

4. **Monitor logs**
   - `tail -f logs/asset_tracking.log`

5. **Keep dependencies updated**
   - Periodically run `pip list --outdated`

6. **Use HTTPS in production**
   - Use Let's Encrypt for free SSL

---

## 🆘 Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   tail -f logs/asset_tracking.log
   ```

2. **Check Django errors:**
   - Error messages in terminal

3. **Read documentation:**
   - README.md
   - QUICKSTART.md
   - BUILD_SUMMARY.md

4. **Google the error:**
   - Most Django errors have solutions online

5. **Check environment:**
   ```bash
   python manage.py check
   ```

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python virtual environment created
- [ ] Dependencies installed
- [ ] MySQL database created
- [ ] .env file configured
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Development server running
- [ ] Can access http://localhost:8000/
- [ ] Can login with admin credentials
- [ ] Can access Django admin
- [ ] Categories created
- [ ] Locations created
- [ ] First asset created
- [ ] Barcode printed successfully

---

## 🎉 You're Ready!

Congratulations! Your Asset Tracking System is now running.

**Next:**
1. Add more categories and locations
2. Create assets
3. Test barcode scanning
4. Invite team members
5. Start tracking assets!

---

## 📞 Support Resources

| Resource | Link |
|----------|------|
| **Project Docs** | README.md |
| **Quick Start** | QUICKSTART.md |
| **Build Summary** | BUILD_SUMMARY.md |
| **Django Docs** | https://docs.djangoproject.com/ |
| **DRF Docs** | https://www.django-rest-framework.org/ |

---

**Happy Asset Tracking! 🚀**

*Version 1.0.0 - March 2026*
