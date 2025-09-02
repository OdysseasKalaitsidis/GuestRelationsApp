# Schema Comparison: MySQL vs PostgreSQL (Supabase)

## Table Structure Comparison

### Users Table
| Feature | MySQL | PostgreSQL (Supabase) | Notes |
|---------|-------|----------------------|-------|
| Primary Key | `id INT AUTO_INCREMENT` | `id SERIAL PRIMARY KEY` | SERIAL is PostgreSQL's AUTO_INCREMENT |
| Username | `VARCHAR(255) UNIQUE` | `VARCHAR(255) UNIQUE` | ✅ Compatible |
| Email | `VARCHAR(255) UNIQUE` | `VARCHAR(255) UNIQUE` | ✅ Compatible |
| Password | `VARCHAR(255)` | `VARCHAR(255)` | ✅ Compatible |
| Admin Flag | `TINYINT(1)` | `BOOLEAN` | ✅ Convert TINYINT(1) to BOOLEAN |
| Timestamps | Manual strings | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | ✅ Better in PostgreSQL |

### Cases Table
| Feature | MySQL | PostgreSQL (Supabase) | Notes |
|---------|-------|----------------------|-------|
| Primary Key | `id INT AUTO_INCREMENT` | `id SERIAL PRIMARY KEY` | ✅ Compatible |
| Room | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |
| Status | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |
| Title | `TEXT` | `TEXT` | ✅ Compatible |
| Owner ID | `INT` | `INTEGER` | ✅ Compatible |
| AI Fields | `VARCHAR(255)` | `VARCHAR(255)` | ✅ Compatible |

### Followups Table
| Feature | MySQL | PostgreSQL (Supabase) | Notes |
|---------|-------|----------------------|-------|
| Primary Key | `id INT AUTO_INCREMENT` | `id SERIAL PRIMARY KEY` | ✅ Compatible |
| Case ID | `INT` | `INTEGER` | ✅ Compatible |
| Suggestion | `TEXT` | `TEXT` | ✅ Compatible |
| Assigned To | `INT` | `INTEGER` | ✅ Compatible |
| Foreign Keys | `ON DELETE CASCADE` | `ON DELETE CASCADE` | ✅ Compatible |

### Tasks Table
| Feature | MySQL | PostgreSQL (Supabase) | Notes |
|---------|-------|----------------------|-------|
| Primary Key | `id INT AUTO_INCREMENT` | `id SERIAL PRIMARY KEY` | ✅ Compatible |
| Title | `VARCHAR(255)` | `VARCHAR(255)` | ✅ Compatible |
| Description | `TEXT` | `TEXT` | ✅ Compatible |
| Task Type | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |
| Due Date | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |
| Status | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |

### Documents Table
| Feature | MySQL | PostgreSQL (Supabase) | Notes |
|---------|-------|----------------------|-------|
| Primary Key | `id INT AUTO_INCREMENT` | `id SERIAL PRIMARY KEY` | ✅ Compatible |
| Filename | `VARCHAR(255)` | `VARCHAR(255)` | ✅ Compatible |
| File Type | `VARCHAR(50)` | `VARCHAR(50)` | ✅ Compatible |
| Content | `TEXT` | `TEXT` | ✅ Compatible |
| File Size | `INT` | `INTEGER` | ✅ Compatible |

## Key Differences and Migration Notes

### 1. AUTO_INCREMENT → SERIAL
```sql
-- MySQL
id INT AUTO_INCREMENT PRIMARY KEY

-- PostgreSQL
id SERIAL PRIMARY KEY
```

### 2. TINYINT(1) → BOOLEAN
```sql
-- MySQL
is_admin TINYINT(1) DEFAULT 0

-- PostgreSQL
is_admin BOOLEAN DEFAULT FALSE
```

### 3. UNSIGNED Integers
```sql
-- MySQL supports UNSIGNED
id INT UNSIGNED AUTO_INCREMENT

-- PostgreSQL doesn't have UNSIGNED
id SERIAL PRIMARY KEY  -- SERIAL is always positive
```

### 4. ENUM Types
```sql
-- Both MySQL and PostgreSQL support ENUM
status ENUM('pending', 'in_progress', 'completed')
```

### 5. Indexes
```sql
-- Both support similar index syntax
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_cases_owner_id ON cases(owner_id);
```

### 6. Foreign Keys
```sql
-- Both support foreign key constraints
owner_id INTEGER REFERENCES users(id)
```

## Migration Strategy

### Automatic Migration (pgloader)
- Use pgloader for bulk schema and data migration
- Handles most type conversions automatically
- May need manual fixes for complex cases

### Manual Fixes Required
1. **Sequences**: Fix AUTO_INCREMENT sequences after migration
2. **Boolean Types**: Ensure TINYINT(1) → BOOLEAN conversion
3. **Timestamps**: Add proper timestamp columns
4. **Indexes**: Verify all indexes are recreated
5. **Foreign Keys**: Ensure constraints are properly set

### Verification Queries
```sql
-- Check sequences
SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT MAX(id) FROM users));

-- Verify data types
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'users';

-- Check foreign keys
SELECT * FROM information_schema.table_constraints 
WHERE constraint_type = 'FOREIGN KEY';
```

## Performance Considerations

### Indexes
- All existing indexes should be recreated
- PostgreSQL may create additional indexes automatically
- Monitor query performance after migration

### Data Types
- PostgreSQL's TEXT type is more efficient than MySQL's
- SERIAL is more efficient than AUTO_INCREMENT
- Boolean types are more space-efficient

### Connection Pooling
- Use asyncpg for better performance
- Configure appropriate pool sizes
- Monitor connection usage

## Compatibility Matrix

| Feature | MySQL | PostgreSQL | Migration Status |
|---------|-------|-----------|------------------|
| Primary Keys | ✅ | ✅ | ✅ Compatible |
| Foreign Keys | ✅ | ✅ | ✅ Compatible |
| Indexes | ✅ | ✅ | ✅ Compatible |
| Text Types | ✅ | ✅ | ✅ Compatible |
| Auto Increment | ✅ | ✅ | ✅ Compatible |
| Boolean Types | ⚠️ | ✅ | ⚠️ Manual Fix |
| Unsigned Ints | ✅ | ❌ | ⚠️ Remove UNSIGNED |
| ENUM Types | ✅ | ✅ | ✅ Compatible |
| JSON Types | ✅ | ✅ | ✅ Compatible |
| Full Text Search | ✅ | ✅ | ✅ Compatible |

## Conclusion
The schema migration from MySQL to PostgreSQL (Supabase) is **highly compatible** with minimal manual intervention required. The main areas requiring attention are:

1. Boolean type conversion
2. Sequence setup
3. Timestamp column addition
4. Performance monitoring

The migration should be straightforward with proper planning and testing.
