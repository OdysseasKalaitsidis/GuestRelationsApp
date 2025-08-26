@echo off
REM Railway Deployment Script for Windows
REM This script helps with common Railway deployment tasks

echo 🚀 Railway Deployment Helper
echo ==============================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI is not installed.
    echo Please install it from: https://docs.railway.app/develop/cli
    pause
    exit /b 1
)

REM Check if user is logged in
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Not logged in to Railway.
    echo Please run: railway login
    pause
    exit /b 1
)

echo ✅ Railway CLI is installed and you're logged in.

:menu
echo.
echo What would you like to do?
echo 1) Run database migrations
echo 2) Check application health
echo 3) View logs
echo 4) Open Railway dashboard
echo 5) Deploy latest changes
echo 6) Exit

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto migrations
if "%choice%"=="2" goto health
if "%choice%"=="3" goto logs
if "%choice%"=="4" goto dashboard
if "%choice%"=="5" goto deploy
if "%choice%"=="6" goto exit
echo ❌ Invalid choice. Please try again.
goto menu

:migrations
echo 🔄 Running database migrations...
railway run --service backend "cd backend && alembic upgrade head"
echo ✅ Database migrations completed.
pause
goto menu

:health
echo 🏥 Checking application health...
railway status
echo ✅ Health check completed.
pause
goto menu

:logs
echo 📋 Viewing recent logs...
railway logs --tail 50
pause
goto menu

:dashboard
echo 🌐 Opening Railway dashboard...
railway open
goto menu

:deploy
echo 🚀 Deploying latest changes...
git push origin main
echo ✅ Deployment triggered. Check Railway dashboard for progress.
pause
goto menu

:exit
echo 👋 Goodbye!
exit /b 0
