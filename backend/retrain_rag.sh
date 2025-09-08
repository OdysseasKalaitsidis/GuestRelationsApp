#!/bin/bash

# RAG Retraining Script
# Automatically retrains the RAG system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
METHOD="rebuild"
DATA_FOLDER="data"
BASE_URL="http://localhost:8000"
API_KEY=""
VERBOSE=false

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -m, --method METHOD     Retraining method: 'rebuild' (default) or 'upload'"
    echo "  -d, --data-folder PATH Path to data folder (default: 'data')"
    echo "  -u, --base-url URL     Base URL of API server (default: 'http://localhost:8000')"
    echo "  -k, --api-key KEY      API key for authentication"
    echo "  -v, --verbose          Enable verbose output"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Retrain using rebuild method"
    echo "  $0 -m upload                          # Retrain using clear and re-upload method"
    echo "  $0 -d /path/to/data -v               # Use custom data folder with verbose output"
    echo "  $0 -u https://api.example.com -k key # Use remote API with authentication"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--method)
            METHOD="$2"
            shift 2
            ;;
        -d|--data-folder)
            DATA_FOLDER="$2"
            shift 2
            ;;
        -u|--base-url)
            BASE_URL="$2"
            shift 2
            ;;
        -k|--api-key)
            API_KEY="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate method
if [[ "$METHOD" != "rebuild" && "$METHOD" != "upload" ]]; then
    print_error "Invalid method: $METHOD. Use 'rebuild' or 'upload'"
    exit 1
fi

# Check if Python script exists
SCRIPT_PATH="retrain_rag.py"
if [[ ! -f "$SCRIPT_PATH" ]]; then
    print_error "Python script '$SCRIPT_PATH' not found!"
    exit 1
fi

# Check if data folder exists
if [[ ! -d "$DATA_FOLDER" ]]; then
    print_error "Data folder '$DATA_FOLDER' does not exist!"
    exit 1
fi

# Build Python command
PYTHON_CMD="python3 $SCRIPT_PATH --method $METHOD --data-folder $DATA_FOLDER --base-url $BASE_URL"

if [[ -n "$API_KEY" ]]; then
    PYTHON_CMD="$PYTHON_CMD --api-key $API_KEY"
fi

if [[ "$VERBOSE" == true ]]; then
    PYTHON_CMD="$PYTHON_CMD --verbose"
fi

# Print configuration
print_info "RAG Retraining Configuration:"
print_info "  Method: $METHOD"
print_info "  Data Folder: $DATA_FOLDER"
print_info "  Base URL: $BASE_URL"
print_info "  API Key: ${API_KEY:+[SET]}${API_KEY:-[NOT SET]}"
print_info "  Verbose: $VERBOSE"
echo ""

# Check if server is running
print_info "Checking if API server is running..."
if curl -s --connect-timeout 5 "$BASE_URL/api/health" > /dev/null 2>&1; then
    print_success "API server is running"
else
    print_warning "Could not connect to API server at $BASE_URL"
    print_warning "Make sure the backend server is running before retraining"
    echo ""
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Retraining cancelled"
        exit 0
    fi
fi

# Run the Python script
print_info "Starting RAG retraining..."
echo ""

if eval $PYTHON_CMD; then
    print_success "RAG retraining completed successfully!"
    echo ""
    print_info "You can now test the RAG system by:"
    print_info "  1. Using the frontend RAG page"
    print_info "  2. Calling the API endpoints directly"
    print_info "  3. Running: curl -X POST $BASE_URL/api/rag/test-rag"
else
    print_error "RAG retraining failed!"
    exit 1
fi
