#!/bin/bash

# Railway Deployment Script
# This script helps with common Railway deployment tasks

set -e

echo "🚀 Railway Deployment Helper"
echo "=============================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed."
    echo "Please install it from: https://docs.railway.app/develop/cli"
    exit 1
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway."
    echo "Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI is installed and you're logged in."

# Function to run database migrations
run_migrations() {
    echo "🔄 Running database migrations..."
    railway run --service backend "cd backend && alembic upgrade head"
    echo "✅ Database migrations completed."
}

# Function to check application health
check_health() {
    echo "🏥 Checking application health..."
    if railway status | grep -q "healthy"; then
        echo "✅ Application is healthy."
    else
        echo "❌ Application health check failed."
        echo "Check the logs with: railway logs"
    fi
}

# Function to view logs
view_logs() {
    echo "📋 Viewing recent logs..."
    railway logs --tail 50
}

# Function to open Railway dashboard
open_dashboard() {
    echo "🌐 Opening Railway dashboard..."
    railway open
}

# Main menu
echo ""
echo "What would you like to do?"
echo "1) Run database migrations"
echo "2) Check application health"
echo "3) View logs"
echo "4) Open Railway dashboard"
echo "5) Deploy latest changes"
echo "6) Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        run_migrations
        ;;
    2)
        check_health
        ;;
    3)
        view_logs
        ;;
    4)
        open_dashboard
        ;;
    5)
        echo "🚀 Deploying latest changes..."
        git push origin main
        echo "✅ Deployment triggered. Check Railway dashboard for progress."
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
