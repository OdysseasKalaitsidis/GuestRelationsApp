# RAG Retraining Scripts

This directory contains automated scripts to retrain the RAG (Retrieval-Augmented Generation) system.

## Files

- `retrain_rag.py` - Main Python script for retraining
- `retrain_rag.sh` - Unix/Linux shell script wrapper
- `retrain_rag.bat` - Windows batch script wrapper

## Quick Start

### Option 1: Using the Shell Script (Unix/Linux/Mac)

```bash
# Make the script executable
chmod +x retrain_rag.sh

# Retrain using default settings (rebuild method)
./retrain_rag.sh

# Retrain using upload method
./retrain_rag.sh -m upload

# Retrain with verbose output
./retrain_rag.sh -v

# Retrain with custom data folder
./retrain_rag.sh -d /path/to/your/data
```

### Option 2: Using the Batch Script (Windows)

```cmd
# Retrain using default settings (rebuild method)
retrain_rag.bat

# Retrain using upload method
retrain_rag.bat -m upload

# Retrain with verbose output
retrain_rag.bat -v

# Retrain with custom data folder
retrain_rag.bat -d C:\path\to\your\data
```

### Option 3: Using Python Directly

```bash
# Retrain using default settings
python3 retrain_rag.py

# Retrain using upload method
python3 retrain_rag.py --method upload

# Retrain with verbose output
python3 retrain_rag.py --verbose

# Retrain with custom settings
python3 retrain_rag.py --method upload --data-folder data --base-url http://localhost:8000 --verbose
```

## Retraining Methods

### Method 1: Rebuild (Default)
- Rebuilds the vectorstore from all documents in the data folder
- Faster and more efficient
- Recommended for most use cases

```bash
./retrain_rag.sh -m rebuild
```

### Method 2: Upload
- Clears the existing collection
- Re-uploads all documents from the data folder
- More thorough but slower
- Use when you want to ensure a clean rebuild

```bash
./retrain_rag.sh -m upload
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-m, --method` | Retraining method: 'rebuild' or 'upload' | 'rebuild' |
| `-d, --data-folder` | Path to data folder containing training documents | 'data' |
| `-u, --base-url` | Base URL of the API server | 'http://localhost:8000' |
| `-k, --api-key` | API key for authentication | None |
| `-v, --verbose` | Enable verbose output | False |
| `-h, --help` | Show help message | - |

## Prerequisites

1. **Backend Server Running**: Make sure your backend server is running on the specified URL
2. **Python Dependencies**: Ensure all required Python packages are installed
3. **Training Documents**: Have training documents in the data folder
4. **API Access**: Ensure you have access to the RAG API endpoints

## Training Documents

The script will automatically process all supported documents in the data folder:

- **Supported formats**: .txt, .md, .pdf, .doc, .docx
- **Location**: `backend/data/` (or custom path specified with `-d`)
- **Current documents**:
  - `hotel_guidelines.md`
  - `Domes_of_Corfu_Marriott_Policies.txt`
  - `Marriott 2024.pdf`
  - `resort_general_info.txt`
  - `RoomTypes.txt`
  - `vip_welcome.txt`
  - `CheckIn.txt`

## Verification

After retraining, the script will:

1. **Get collection stats** to show the number of chunks processed
2. **Test the RAG system** to ensure it's working correctly
3. **Report success/failure** with detailed logging

## Troubleshooting

### Common Issues

1. **Server not running**
   ```
   ERROR: Could not connect to API server
   ```
   **Solution**: Start your backend server before running the script

2. **No documents found**
   ```
   ERROR: No supported documents found in 'data'
   ```
   **Solution**: Ensure you have training documents in the data folder

3. **Permission denied**
   ```
   ERROR: Permission denied
   ```
   **Solution**: Make sure the script has read access to the data folder

4. **Python not found**
   ```
   ERROR: python3: command not found
   ```
   **Solution**: Install Python 3 or use `python` instead of `python3`

### Debug Mode

Use the `--verbose` flag to get detailed logging:

```bash
./retrain_rag.sh -v
```

## Examples

### Basic Retraining
```bash
./retrain_rag.sh
```

### Complete Retrain with Upload Method
```bash
./retrain_rag.sh -m upload -v
```

### Custom Data Folder
```bash
./retrain_rag.sh -d /path/to/custom/data -v
```

### Remote API Server
```bash
./retrain_rag.sh -u https://api.example.com -k your-api-key
```

## Integration

You can integrate this script into your deployment pipeline:

```bash
# In your deployment script
echo "Retraining RAG system..."
./retrain_rag.sh -m upload -v
if [ $? -eq 0 ]; then
    echo "RAG retraining successful"
else
    echo "RAG retraining failed"
    exit 1
fi
```

## Automation

### Cron Job (Unix/Linux)
```bash
# Add to crontab to retrain daily at 2 AM
0 2 * * * /path/to/backend/retrain_rag.sh -m rebuild
```

### Windows Task Scheduler
Create a scheduled task to run `retrain_rag.bat` at regular intervals.

## Support

If you encounter issues:

1. Check the verbose output: `./retrain_rag.sh -v`
2. Verify your backend server is running
3. Ensure all training documents are accessible
4. Check the API endpoints manually: `curl http://localhost:8000/api/rag/stats`
