#!/bin/bash
# Asset Tracking System Startup Script

echo "================================"
echo "Asset Tracking System - Startup"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Creating .env from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit .env with your database credentials"
    echo ""
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input
echo "✅ Migrations completed"
echo ""

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear -q
echo "✅ Static files collected"
echo ""

# Start server
echo "🚀 Starting development server..."
echo ""
echo "========================================"
echo "Asset Tracking System is running!"
echo "========================================"
echo ""
echo "📍 Access at: http://localhost:8000"
echo "👤 Admin:    http://localhost:8000/admin/"
echo "🔐 Login:    http://localhost:8000/login/"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python manage.py runserver
