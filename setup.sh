#!/bin/bash
# Quick Setup Script for Agricultural Platform Upgrade
# This script sets up the development environment with new requirements

echo "🚀 Agricultural Platform - Phase 1 Setup Script"
echo "=============================================="

# Check if Python 3.11+ is installed
python_version=$(python --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
if [[ $(echo "$python_version >= 3.11" | bc -l) -eq 1 ]]; then
    echo "✅ Python $python_version detected"
else
    echo "❌ Python 3.11+ required. Current version: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install development requirements
echo "📦 Installing development requirements..."
pip install -r requirements-dev.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration"
fi

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p backups
mkdir -p media/uploads

# Run Django checks
echo "🔍 Running Django system checks..."
python manage.py check

# Check if database migration is needed
echo "🔍 Checking database status..."
if [ -f "db.sqlite3" ]; then
    echo "📊 SQLite database found - migration recommended"
    echo "📝 Run: python scripts/migrate_to_postgresql.py"
else
    echo "✅ No SQLite database found"
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configuration"
echo "2. Run database migration: python scripts/migrate_to_postgresql.py"
echo "3. Start development server: python manage.py runserver"
echo ""
