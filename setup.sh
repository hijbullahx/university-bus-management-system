#!/bin/bash
# Quick Setup Script for IUBAT Bus Management System

echo "🚌 IUBAT Bus Management System - Quick Setup"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please create it first:"
    echo "  cd .."
    echo "  python -m venv venv"
    exit 1
fi

echo "✓ Virtual environment found"

# Activate virtual environment
source ../venv/Scripts/activate

echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r Requirements.txt --quiet

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (please edit with your settings)"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "✓ Migrations complete"

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "✓ Static files collected"

echo ""
echo "=============================================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Run server: python manage.py runserver"
echo "3. Visit http://127.0.0.1:8000/"
echo "4. Test simulation: python manage.py simulate_bus_gps"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for more details"
