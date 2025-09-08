@echo off
REM RAG Retraining Script for Windows
REM Automatically retrains the RAG system

setlocal enabledelayedexpansion

REM Default values
set METHOD=rebuild
set DATA_FOLDER=data
set BASE_URL=http://localhost:8000
set API_KEY=
set VERBOSE=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :run_script
if "%~1"=="-m" (
    set METHOD=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--method" (
    set METHOD=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-d" (
    set DATA_FOLDER=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--data-folder" (
    set DATA_FOLDER=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-u" (
    set BASE_URL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--base-url" (
    set BASE_URL=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-k" (
    set API_KEY=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="--api-key" (
    set API_KEY=%~2
    shift
    shift
    goto :parse_args
)
if "%~1"=="-v" (
    set VERBOSE=true
    shift
    goto :parse_args
)
if "%~1"=="--verbose" (
    set VERBOSE=true
    shift
    goto :parse_args
)
if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help
echo Unknown option: %~1
goto :show_help

:show_help
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   -m, --method METHOD     Retraining method: 'rebuild' (default) or 'upload'
echo   -d, --data-folder PATH Path to data folder (default: 'data')
echo   -u, --base-url URL     Base URL of API server (default: 'http://localhost:8000')
echo   -k, --api-key KEY      API key for authentication
echo   -v, --verbose          Enable verbose output
echo   -h, --help             Show this help message
echo.
echo Examples:
echo   %0                                    # Retrain using rebuild method
echo   %0 -m upload                          # Retrain using clear and re-upload method
echo   %0 -d C:\path\to\data -v              # Use custom data folder with verbose output
echo   %0 -u https://api.example.com -k key  # Use remote API with authentication
goto :eof

:run_script
REM Validate method
if not "%METHOD%"=="rebuild" if not "%METHOD%"=="upload" (
    echo ERROR: Invalid method: %METHOD%. Use 'rebuild' or 'upload'
    exit /b 1
)

REM Check if Python script exists
if not exist "retrain_rag.py" (
    echo ERROR: Python script 'retrain_rag.py' not found!
    exit /b 1
)

REM Check if data folder exists
if not exist "%DATA_FOLDER%" (
    echo ERROR: Data folder '%DATA_FOLDER%' does not exist!
    exit /b 1
)

REM Print configuration
echo [INFO] RAG Retraining Configuration:
echo [INFO]   Method: %METHOD%
echo [INFO]   Data Folder: %DATA_FOLDER%
echo [INFO]   Base URL: %BASE_URL%
if defined API_KEY (
    echo [INFO]   API Key: [SET]
) else (
    echo [INFO]   API Key: [NOT SET]
)
echo [INFO]   Verbose: %VERBOSE%
echo.

REM Check if server is running
echo [INFO] Checking if API server is running...
curl -s --connect-timeout 5 "%BASE_URL%/api/health" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] API server is running
) else (
    echo [WARNING] Could not connect to API server at %BASE_URL%
    echo [WARNING] Make sure the backend server is running before retraining
    echo.
    set /p CONTINUE="Do you want to continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo [INFO] Retraining cancelled
        exit /b 0
    )
)

REM Build Python command
set PYTHON_CMD=python retrain_rag.py --method %METHOD% --data-folder %DATA_FOLDER% --base-url %BASE_URL%

if defined API_KEY (
    set PYTHON_CMD=!PYTHON_CMD! --api-key %API_KEY%
)

if "%VERBOSE%"=="true" (
    set PYTHON_CMD=!PYTHON_CMD! --verbose
)

REM Run the Python script
echo [INFO] Starting RAG retraining...
echo.

%PYTHON_CMD%
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] RAG retraining completed successfully!
    echo.
    echo [INFO] You can now test the RAG system by:
    echo [INFO]   1. Using the frontend RAG page
    echo [INFO]   2. Calling the API endpoints directly
    echo [INFO]   3. Running: curl -X POST %BASE_URL%/api/rag/test-rag
) else (
    echo.
    echo [ERROR] RAG retraining failed!
    exit /b 1
)

endlocal
