#!/bin/bash

# Development Setup Script for Guest Relations System
# This script sets up the development environment

set -e  # Exit on any error

echo "🛠️  Setting up development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL 8.0+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Backend setup
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
DATABASE_URL=mysql+pymysql://myuser:Odkalaitsidis12%2540@localhost:3306/mydb
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-here
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
ENVIRONMENT=development
EOF
    echo "⚠️  Please edit backend/.env with your actual configuration"
fi

cd ..

# Frontend setup
echo "⚛️  Setting up React frontend..."
cd frontend

# Install dependencies
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating frontend .env file..."
    cat > .env << EOF
VITE_API_URL=http://localhost:8000/api
EOF
fi

cd ..

echo "✅ Development environment setup completed!"
echo ""
echo "🚀 To start the development servers:"
echo ""
echo "Backend (Terminal 1):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "Frontend (Terminal 2):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "📝 Don't forget to:"
echo "  1. Set up your MySQL database"
echo "  2. Run database migrations: cd backend && alembic upgrade head"
echo "  3. Seed initial data: cd backend && python seed_users.py"
echo "  4. Add your OpenAI API key to backend/.env"
