# 🚀 Migration Roadmap: FastAPI + MySQL → Supabase (Postgres)

## Current State Analysis

### Database Schema
- **Tables**: users, cases, followups, tasks, documents
- **Relationships**: Foreign keys between users and other tables
- **Current Driver**: PyMySQL with MySQL
- **Migration Tool**: Alembic (4 existing migrations)

### Key MySQL Features to Migrate
- `AUTO_INCREMENT` → `SERIAL` or `BIGSERIAL`
- `TINYINT(1)` → `BOOLEAN`
- `VARCHAR(255)` → `VARCHAR(255)` (compatible)
- `TEXT` → `TEXT` (compatible)
- `ENUM` → `ENUM` (Postgres supports this)
- `UNSIGNED` integers → regular integers (Postgres doesn't have unsigned)

## Phase 1: Preparation ✅

### Inventory Current MySQL Schema
```sql
-- Run these queries to inventory your current schema
SHOW TABLES;
SHOW CREATE TABLE users;
SHOW CREATE TABLE cases;
SHOW CREATE TABLE followups;
SHOW CREATE TABLE tasks;
SHOW CREATE TABLE documents;
SHOW INDEX FROM users;
SHOW INDEX FROM cases;
SHOW INDEX FROM followups;
SHOW INDEX FROM tasks;
SHOW INDEX FROM documents;
```

### Create Migration Repository Structure
```
migration/
├── README.md (this file)
├── scripts/
│   ├── 01_inventory_schema.sql
│   ├── 02_export_data.sql
│   ├── 03_supabase_setup.sql
│   └── 04_verify_migration.sql
├── config/
│   ├── .env.template
│   └── supabase_config.json
└── docs/
    ├── schema_comparison.md
    └── migration_checklist.md
```

### Freeze Features
- Announce maintenance window
- Stop new feature development
- Create backup of current database

## Phase 2: Set Up Supabase

### Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Note down:
   - Project URL -> https://sjjuaesddqzfcdahutfl.supabase.co
   - Database password Odysseaskal
   - Anon key
   - Service role key

### Enable Required Extensions
```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Environment Variables Template
```bash
# .env.template
DATABASE_URL="postgresql+asyncpg://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres?sslmode=require"
SUPABASE_URL="https://PROJECT_ID.supabase.co"
SUPABASE_ANON_KEY="your_anon_key"
SUPABASE_SERVICE_ROLE_KEY="your_service_role_key"
```

## Phase 3: Schema Migration

### Export MySQL Schema
```bash
# Export schema only
mysqldump -u USER -p --no-data --routines --triggers YOUR_DB > schema_only.sql

# Export data only
mysqldump -u USER -p --no-create-info --no-create-db --no-create-table YOUR_DB > data_only.sql
```

### Use pgloader for Auto-Conversion
```bash
# Install pgloader
# Ubuntu/Debian: sudo apt-get install pgloader
# macOS: brew install pgloader

# Run migration
pgloader mysql://USER:PASS@MYSQL_HOST/DB_NAME \
         postgresql://postgres:PASS@db.PROJECT_ID.supabase.co:5432/postgres
```

### Manual Schema Fixes (if needed)
```sql
-- Fix AUTO_INCREMENT sequences
SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('cases', 'id'), (SELECT MAX(id) FROM cases));
SELECT setval(pg_get_serial_sequence('followups', 'id'), (SELECT MAX(id) FROM followups));
SELECT setval(pg_get_serial_sequence('tasks', 'id'), (SELECT MAX(id) FROM tasks));
SELECT setval(pg_get_serial_sequence('documents', 'id'), (SELECT MAX(id) FROM documents));
```

## Phase 4: Data Migration

### Verify Data Integrity
```sql
-- Compare row counts
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'cases', COUNT(*) FROM cases
UNION ALL
SELECT 'followups', COUNT(*) FROM followups
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'documents', COUNT(*) FROM documents;
```

### Handle Large Data Sets
```bash
# For large tables, use CSV export/import
mysql -u USER -p -e "SELECT * FROM users" > users.csv
# Import via Supabase Table Editor or COPY command
```

## Phase 5: Backend Refactor

### Update Dependencies
```txt
# requirements.txt updates
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0  # Replace pymysql
python-multipart==0.0.6
python-dotenv==1.0.0
openai==1.3.7
alembic==1.12.1
requests==2.31.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
email-validator==2.1.0
reportlab==4.0.7
PyPDF2==3.0.1
scikit-learn==1.2.2
numpy==1.23.5
pdfplumber==0.9.0
python-docx==0.8.11
spacy==3.5.3
supabase==2.0.0  # Add Supabase client
```

### Update Database Connection
```python
# db.py changes
import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()
engine = None
SessionLocal = None
logger = logging.getLogger(__name__)

def get_database_url():
    """Build the SQLAlchemy database URL for Supabase"""
    return os.environ.get("DATABASE_URL")

def initialize_database():
    """Initialize engine and session with Supabase settings"""
    global engine, SessionLocal
    db_url = get_database_url()
    if db_url:
        logger.info("Initializing Supabase database connection")
        
        # Create async engine for Supabase
        engine = create_async_engine(
            db_url,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
        SessionLocal = sessionmaker(bind=engine)
        
        logger.info("Supabase database engine created successfully")
        return True
    else:
        logger.warning("No DATABASE_URL available")
        return False
```

### Update Models (if needed)
```python
# models.py - mostly compatible, but check for:
# 1. ENUM types
# 2. UNSIGNED integers
# 3. MySQL-specific column types
```

## Phase 6: Testing

### Unit Tests
```python
# test_db_migration.py
import pytest
from sqlalchemy import text
from db import get_engine

async def test_database_connection():
    engine = get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

async def test_tables_exist():
    engine = get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        expected_tables = ['users', 'cases', 'followups', 'tasks', 'documents']
        for table in expected_tables:
            assert table in tables
```

### Integration Tests
```python
# test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_users_endpoint():
    response = client.get("/api/users")
    assert response.status_code == 200

def test_cases_endpoint():
    response = client.get("/api/cases")
    assert response.status_code == 200
```

## Phase 7: Deployment

### Choose PaaS
- **Render**: Easy deployment, good for FastAPI
- **Railway**: Already using, good integration
- **Vercel**: Good for serverless

### Deployment Steps
1. Update `requirements.txt`
2. Set environment variables
3. Deploy to chosen platform
4. Run smoke tests

## Phase 8: Cutover

### Pre-Cutover Checklist
- [ ] All tests passing
- [ ] Data verified in Supabase
- [ ] Performance benchmarks met
- [ ] Rollback plan ready

### Cutover Steps
1. Announce maintenance window
2. Stop writes to MySQL
3. Final data sync
4. Update DATABASE_URL
5. Deploy new version
6. Verify all endpoints

## Phase 9: Post-Migration

### Monitoring
- Set up logging for query performance
- Monitor error rates
- Check connection pool usage

### Security
- Enable Row Level Security (RLS) if needed
- Review access patterns
- Set up proper authentication

### Documentation
- Update deployment docs
- Document new database procedures
- Create troubleshooting guide

## Rollback Plan

### Quick Rollback
1. Revert DATABASE_URL to MySQL
2. Deploy previous version
3. Verify data integrity

### Data Recovery
- Keep MySQL backup for 30 days
- Document data sync procedures
- Test rollback procedures

## Timeline Estimate

- **Phase 1-2**: 1-2 days
- **Phase 3-4**: 2-3 days
- **Phase 5-6**: 3-5 days
- **Phase 7**: 1 day
- **Phase 8**: 1 day
- **Phase 9**: Ongoing

**Total**: 8-12 days for complete migration

## Risk Mitigation

1. **Data Loss**: Multiple backups, dry runs
2. **Downtime**: Minimal maintenance window
3. **Performance**: Benchmark before/after
4. **Compatibility**: Test all features thoroughly

## Success Metrics

- [ ] Zero data loss
- [ ] All API endpoints working
- [ ] Performance maintained or improved
- [ ] User experience unchanged
- [ ] Monitoring and logging in place
