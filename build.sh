#!/bin/bash

# Build script for Railway deployment
set -e

echo "🚀 Building Guest Relations System for Railway..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm ci
npm run build
cd ..

# Copy frontend build to backend
echo "📁 Copying frontend build to backend..."
cp -r frontend/dist backend/static

echo "✅ Build completed successfully!"
echo "📁 Frontend build copied to backend/static/"
