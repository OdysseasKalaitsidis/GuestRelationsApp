# Deployment Guide for Supabase Migration

## Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Supabase project created
- [ ] Database credentials secured
- [ ] Environment variables configured
- [ ] Local testing completed
- [ ] All tests passing

### 2. Code Changes
- [ ] Updated requirements.txt (asyncpg instead of pymysql)
- [ ] Updated db.py for async PostgreSQL
- [ ] Updated any MySQL-specific queries
- [ ] Models compatible with PostgreSQL
- [ ] Alembic migrations updated

### 3. Data Migration
- [ ] MySQL data exported and backed up
- [ ] Data imported to Supabase
- [ ] Row counts verified
- [ ] Foreign key relationships intact
- [ ] Sequences properly set

## Deployment Platforms

### Option 1: Railway (Recommended - Already Using)
```bash
# 1. Update requirements.txt
cp migration/requirements-supabase.txt backend/requirements.txt

# 2. Update environment variables in Railway dashboard
DATABASE_URL="postgresql+asyncpg://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres?sslmode=require"
SUPABASE_URL="https://PROJECT_ID.supabase.co"
SUPABASE_ANON_KEY="your_anon_key"
SUPABASE_SERVICE_ROLE_KEY="your_service_role_key"

# 3. Deploy
git add .
git commit -m "Migrate to Supabase PostgreSQL"
git push
```

### Option 2: Render
```yaml
# render.yaml
services:
  - type: web
    name: guest-relations-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: postgresql+asyncpg://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres?sslmode=require
      - key: SUPABASE_URL
        value: https://PROJECT_ID.supabase.co
      - key: SUPABASE_ANON_KEY
        value: your_anon_key
      - key: SUPABASE_SERVICE_ROLE_KEY
        value: your_service_role_key
```

### Option 3: Vercel
```json
// vercel.json
{
  "functions": {
    "backend/main.py": {
      "runtime": "python3.9"
    }
  },
  "env": {
    "DATABASE_URL": "postgresql+asyncpg://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres?sslmode=require",
    "SUPABASE_URL": "https://PROJECT_ID.supabase.co",
    "SUPABASE_ANON_KEY": "your_anon_key",
    "SUPABASE_SERVICE_ROLE_KEY": "your_service_role_key"
  }
}
```

## Environment Variables

### Required Variables
```bash
# Database
DATABASE_URL="postgresql+asyncpg://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres?sslmode=require"

# Supabase
SUPABASE_URL="https://PROJECT_ID.supabase.co"
SUPABASE_ANON_KEY="your_anon_key"
SUPABASE_SERVICE_ROLE_KEY="your_service_role_key"

# Application
SECRET_KEY="your_secret_key"
OPENAI_API_KEY="your_openai_api_key"
ENVIRONMENT="production"

# CORS
ALLOWED_ORIGINS="https://guestreationadomes.netlify.app,http://localhost:5173"
```

### Optional Variables
```bash
# Database Pool Settings
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600

# Logging
LOG_LEVEL="INFO"
LOG_FORMAT="json"

# Railway (if using)
RAILWAY_PUBLIC_DOMAIN="your_railway_domain"
```

## Deployment Steps

### Step 1: Prepare Code
```bash
# 1. Update requirements.txt
cp migration/requirements-supabase.txt backend/requirements.txt

# 2. Update db.py
cp migration/db_supabase.py backend/db.py

# 3. Test locally
cd backend
pip install -r requirements.txt
python -m pytest tests/  # if you have tests
uvicorn main:app --reload
```

### Step 2: Deploy to Staging
```bash
# 1. Create staging environment
# 2. Deploy with staging DATABASE_URL
# 3. Run smoke tests
# 4. Verify all endpoints work
```

### Step 3: Deploy to Production
```bash
# 1. Announce maintenance window
# 2. Stop writes to MySQL
# 3. Final data sync
# 4. Update DATABASE_URL to Supabase
# 5. Deploy new version
# 6. Verify all endpoints
# 7. Monitor for issues
```

## Testing Deployment

### Smoke Tests
```bash
# Test health endpoint
curl https://your-app.railway.app/api/health

# Test database connection
curl https://your-app.railway.app/api/test/db

# Test main endpoints
curl https://your-app.railway.app/api/users
curl https://your-app.railway.app/api/cases
```

### Load Testing
```bash
# Install artillery
npm install -g artillery

# Run load test
artillery quick --count 100 --num 10 https://your-app.railway.app/api/health
```

## Monitoring and Logs

### Railway Logs
```bash
# View logs
railway logs

# Follow logs
railway logs --follow
```

### Supabase Monitoring
- Check Supabase dashboard for:
  - Database performance
  - Connection usage
  - Query performance
  - Error rates

### Application Monitoring
```python
# Add to main.py for better monitoring
import logging
from fastapi import Request
import time

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s"
    )
    return response
```

## Rollback Plan

### Quick Rollback
```bash
# 1. Revert DATABASE_URL to MySQL
DATABASE_URL="mysql+pymysql://user:pass@host:3306/db"

# 2. Deploy previous version
git revert HEAD
git push

# 3. Verify rollback
curl https://your-app.railway.app/api/health
```

### Data Recovery
```bash
# If data loss occurs
# 1. Restore from MySQL backup
# 2. Re-run migration
# 3. Verify data integrity
```

## Post-Deployment Checklist

- [ ] All endpoints responding correctly
- [ ] Database queries performing well
- [ ] No errors in logs
- [ ] User experience unchanged
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Team notified of changes
- [ ] Backup procedures updated

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   ```bash
   # Check DATABASE_URL format
   # Verify Supabase credentials
   # Check network connectivity
   ```

2. **SSL Issues**
   ```bash
   # Ensure sslmode=require in DATABASE_URL
   # Check Supabase SSL configuration
   ```

3. **Pool Exhaustion**
   ```bash
   # Reduce pool_size
   # Increase max_overflow
   # Check for connection leaks
   ```

4. **Performance Issues**
   ```bash
   # Check query performance in Supabase dashboard
   # Verify indexes are created
   # Monitor connection usage
   ```

### Support Contacts
- Supabase Support: https://supabase.com/support
- Railway Support: https://railway.app/support
- Your team's emergency contacts
