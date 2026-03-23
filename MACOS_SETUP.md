# 🍎 macOS Setup Guide - Asset Tracking System

## ⚠️ macOS-Specific Setup Required

macOS requires additional setup before you can install dependencies. Follow this guide carefully.

---

## 📋 Step 1: Install Homebrew (if not already installed)

```bash
# Check if Homebrew is installed
brew --version

# If not installed, install it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

## 🍎 Step 2: Install MySQL via Homebrew

```bash
# Update Homebrew
brew update

# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Verify installation
mysql --version

# Test connection (no password for default setup)
mysql -u root
# Type: EXIT; to quit
```

---

## 🐍 Step 3: Install Python 3 (if needed)

```bash
# Check Python version
python3 --version

# If Python 3.8+ is not installed
brew install python@3.11

# Verify
python3 --version
```

---

## 📁 Step 4: Navigate to Project

```bash
cd ~/Desktop/asset-tracking-system
```

---

## 🔧 Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

---

## 📦 Step 6: Install Python Dependencies

Now install the requirements:

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

**Expected output:** All packages install successfully (no errors about pkg-config)

If you see any errors, run:
```bash
pip install -r requirements.txt -v
```

---

## 🗄️ Step 7: Setup MySQL Database

### Create Database

```bash
# Connect to MySQL
mysql -u root

# In MySQL console, create database:
CREATE DATABASE asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verify it was created
SHOW DATABASES;

# Exit MySQL
EXIT;
```

### Alternative (One-liner)

```bash
mysql -u root -e "CREATE DATABASE asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

---

## ⚙️ Step 8: Configure Environment

```bash
# Copy .env template
cp .env.example .env

# Edit with your preferred editor
nano .env
```

**Edit `.env` file:**

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=asset_tracking
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

**Note:** Leave `DB_PASSWORD` empty (default MySQL setup on macOS has no password)

Save: Press `Ctrl+X` → `Y` → `Enter`

---

## 🗄️ Step 9: Run Django Migrations

```bash
# Make sure you're in the project directory with venv activated
# You should see (venv) in your terminal

python manage.py makemigrations
python manage.py migrate
```

---

## 👤 Step 10: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

**Example:**
```
Username: admin
Email: admin@example.com
Password: admin123
Password (again): admin123
```

---

## 🎨 Step 11: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Step 12: Start Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🌐 Access the System

Open your browser:

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Dashboard |
| `http://localhost:8000/login/` | Login |
| `http://localhost:8000/admin/` | Admin Panel |

Login with admin credentials you just created.

---

## ✅ Quick Setup Script (One-liner)

Save this as `setup_macos.sh`:

```bash
#!/bin/bash

echo "🍎 Asset Tracking System - macOS Setup"
echo "========================================"

# Check Homebrew
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install MySQL
echo "Installing MySQL..."
brew install mysql
brew services start mysql

# Create database
echo "Creating database..."
mysql -u root -e "CREATE DATABASE IF NOT EXISTS asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Create venv
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Edit .env with your settings if needed"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Create admin: python manage.py createsuperuser"
echo "3. Start server: python manage.py runserver"
echo "4. Open browser: http://localhost:8000"
```

Make it executable and run:
```bash
chmod +x setup_macos.sh
./setup_macos.sh
```

---

## 🆘 Troubleshooting

### Issue: "mysql: command not found"

**Solution:**
```bash
# Install MySQL
brew install mysql

# Start it
brew services start mysql

# Verify
mysql --version
```

### Issue: "Can't connect to MySQL server"

**Solution:**
```bash
# Check if MySQL is running
brew services list

# Start MySQL if stopped
brew services start mysql

# Restart MySQL
brew services restart mysql
```

### Issue: "No module named 'django'"

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: "permission denied" on setup script

**Solution:**
```bash
chmod +x setup_macos.sh
./setup_macos.sh
```

### Issue: "port 8000 already in use"

**Solution:**
```bash
# Use different port
python manage.py runserver 8001
```

### Issue: "database doesn't exist"

**Solution:**
```bash
# Create database
mysql -u root -e "CREATE DATABASE asset_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
python manage.py migrate
```

### Issue: "ERROR: Could not find a version that satisfies the requirement"

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache and reinstall
pip install --upgrade --force-reinstall -r requirements.txt
```

---

## 🔄 Stopping & Restarting

### Stop MySQL
```bash
brew services stop mysql
```

### Stop Django Server
Press `Ctrl+C` in the terminal running the server

### Restart MySQL
```bash
brew services restart mysql
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 📊 Useful Commands

```bash
# Activate venv
source venv/bin/activate

# Deactivate venv
deactivate

# Check MySQL status
brew services list

# Start MySQL
brew services start mysql

# Stop MySQL
brew services stop mysql

# Connect to MySQL
mysql -u root

# Run Django shell
python manage.py shell

# Create admin
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001
```

---

## 🎯 Complete macOS Setup Flow

```
1. Install Homebrew
   ↓
2. Install MySQL
   ↓
3. Start MySQL service
   ↓
4. Create database
   ↓
5. Create Python venv
   ↓
6. Install dependencies
   ↓
7. Configure .env
   ↓
8. Run migrations
   ↓
9. Create admin user
   ↓
10. Collect static files
    ↓
11. Start server
    ↓
12. Access http://localhost:8000
```

---

## ✨ Pro Tips

### Tip 1: Always Activate venv
Before running any commands, activate virtual environment:
```bash
source venv/bin/activate
```

### Tip 2: Keep MySQL Running
MySQL needs to be running for the app to work. Check with:
```bash
brew services list | grep mysql
```

### Tip 3: Use Different Ports
If port 8000 is busy, use:
```bash
python manage.py runserver 8001
```

### Tip 4: Save Your Admin Password
Write down your admin password somewhere safe!

### Tip 5: Regular Backups
Backup your database regularly:
```bash
mysqldump -u root asset_tracking > backup.sql
```

---

## 📚 Additional Resources

- **Homebrew Docs:** https://brew.sh
- **MySQL Docs:** https://dev.mysql.com/doc/
- **Python Docs:** https://docs.python.org/3/
- **Django Docs:** https://docs.djangoproject.com/

---

## 🎉 You're Ready!

Once you complete these steps, your Asset Tracking System will be running!

**Next:**
1. Create categories and locations in admin
2. Create your first asset
3. Print barcode
4. Test scanning

---

**macOS Setup Guide v1.0**
*Optimized for macOS 10.15+ with Homebrew*

**Need help?** Check INSTALLATION.md for general troubleshooting
