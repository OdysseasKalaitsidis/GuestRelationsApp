# Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. Application Startup Failures

**Problem**: Application fails to start with asyncio or import errors

**Solution**: 
- The application now uses lazy loading for spacy models
- Database connection is optional during startup
- Use `python startup.py` to start the application

### 2. Database Connection Issues

**Problem**: Missing MySQL environment variables

**Solution**:
- Set the following environment variables:
  - `MYSQLUSER`
  - `MYSQLPASSWORD` 
  - `MYSQLHOST`
  - `MYSQLDATABASE`
  - `MYSQLPORT` (optional, defaults to 3306)

### 3. Spacy Model Issues

**Problem**: Spacy model not installed

**Solution**:
- The startup script automatically installs the required model
- If manual installation is needed: `python -m spacy download en_core_web_sm`

### 4. Environment Variables

**Required for full functionality**:
```
MYSQLUSER=your_mysql_user
MYSQLPASSWORD=your_mysql_password
MYSQLHOST=your_mysql_host
MYSQLDATABASE=your_database_name
OPENAI_API_KEY=your_openai_api_key
```

**Optional**:
```
ENVIRONMENT=production|development
LOG_LEVEL=INFO|DEBUG|WARNING|ERROR
PORT=8000
```

## Startup Commands

### Development
```bash
python startup.py
```

### Production (Railway/Heroku)
The Procfile uses: `web: python startup.py`

### Testing
```bash
python test_startup.py  # Test imports and app creation
python check_spacy.py   # Test spacy model installation
```

## Recent Fixes Applied

1. **Lazy Loading**: Spacy models are now loaded only when needed
2. **Optional Database**: App can start without database connection
3. **Startup Script**: Handles spacy model installation automatically
4. **Error Handling**: Better error messages and graceful degradation

## Monitoring

Check logs in `logs/app.log` for detailed error information.
