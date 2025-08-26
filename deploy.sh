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
    echo "Creating a basic .env file..."
    cat > backend/.env << EOF
DATABASE_URL=mysql+pymysql://myuser:mypassword@db:3306/mydb
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-here
ALLOWED_ORIGINS=http://localhost,http://localhost:80
ENVIRONMENT=production
LOG_LEVEL=INFO
EOF
    echo "📝 Please edit backend/.env with your actual configuration"
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans || true

# Build and start services
echo "🔨 Building and starting services..."
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 45

# Check if backend is healthy
echo "🏥 Checking backend health..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy"
        break
    else
        echo "⏳ Attempt $attempt/$max_attempts - Backend not ready yet..."
        sleep 10
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Backend health check failed after $max_attempts attempts"
    echo "Checking logs..."
    docker-compose logs backend
    exit 1
fi

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Seed initial data
echo "🌱 Seeding initial data..."
docker-compose exec -T backend python seed_users.py

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
