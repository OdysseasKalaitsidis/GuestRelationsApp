#!/bin/bash

# Production Deployment Script for Guest Relations System
# This script sets up the application for production deployment

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads
mkdir -p ssl
mkdir -p logs

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found in backend directory."
    echo "Please create a .env file with your configuration:"
    echo "cp backend/.env.example backend/.env"
    echo "Then edit backend/.env with your settings."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if backend is healthy
echo "🏥 Checking backend health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "Checking logs..."
    docker-compose logs backend
    exit 1
fi

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec backend alembic upgrade head

# Seed initial data
echo "🌱 Seeding initial data..."
docker-compose exec backend python seed_users.py

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application is now running at:"
echo "   Frontend: http://localhost"
echo "   API: http://localhost/api"
echo "   Health Check: http://localhost/health"
echo ""
echo "📊 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop the application:"
echo "   docker-compose down"
