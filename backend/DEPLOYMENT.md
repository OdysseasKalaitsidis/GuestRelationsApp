# Deployment Troubleshooting Guide

## The Distutils Issue

Python 3.12 removed `distutils` entirely, which causes deployment failures when packages need to be compiled from source. This is a common issue with Nixpacks and other deployment platforms.

## Solutions Implemented

### 1. Python Version Lock
- **Current**: Python 3.12.0 (stable, has distutils)
- **Files**: `nixpacks.json`, `runtime.txt`, `.python-version`

### 2. Package Version Optimization
- **Current**: `requirements.txt` with Python 3.12 compatible versions
- **Fallback**: `requirements-conservative.txt` with very stable versions
- **Strategy**: Use versions with pre-built wheels to avoid compilation

### 3. Build Environment
- **System packages**: All necessary build tools and libraries
- **Environment variables**: Optimized for binary package installation
- **Deployment script**: `deploy.sh` for controlled environment setup

## Deployment Commands

### Primary (Recommended)
```bash
# Use the optimized configuration
nixpacks build .
```

### Fallback (If issues persist)
```bash
# Use conservative package versions
cp requirements-conservative.txt requirements.txt
nixpacks build .
```

### Manual Debug
```bash
# Check Python version
python --version

# Verify virtual environment
which python
pip list

# Test package installation
pip install --only-binary=all -r requirements.txt
```

## Common Issues & Solutions

### Issue: "distutils not found"
**Solution**: Ensure Python 3.12 is used (not 3.11)

### Issue: "Failed to build wheel"
**Solution**: Use `--only-binary=all` flag or update package versions

### Issue: "Missing system dependencies"
**Solution**: Check that all packages in `nixpacks.json` are available

### Issue: "Memory/Timeout during build"
**Solution**: Use conservative requirements or split deployment into stages

## Package-Specific Notes

- **scikit-learn**: Version 1.2.2 has pre-built wheels for Python 3.12
- **numpy**: Version 1.23.5 is stable and widely supported
- **spacy**: Version 3.5.3 works well with Python 3.12
- **fastapi**: Version 0.104.1 is current and stable

## Environment Variables

Key environment variables set in deployment:
- `PYTHON_VERSION=3.12.0`
- `PIP_PREFER_BINARY=1`
- `PIP_NO_CACHE_DIR=1`
- `PYTHONUNBUFFERED=1`

## Monitoring Deployment

Watch for these success indicators:
1. Python 3.12.0 detected
2. Virtual environment created successfully
3. Packages installed from pre-built wheels
4. No compilation errors
5. Application starts without import errors
