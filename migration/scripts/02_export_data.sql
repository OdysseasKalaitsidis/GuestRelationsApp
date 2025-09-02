-- MySQL Data Export Scripts
-- Run these commands to export your data for migration

-- 1. Export schema only (structure without data)
-- Run this command in terminal:
-- mysqldump -u YOUR_USER -p --no-data --routines --triggers YOUR_DATABASE > schema_only.sql

-- 2. Export data only (data without structure)
-- Run this command in terminal:
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE > data_only.sql

-- 3. Export complete database
-- Run this command in terminal:
-- mysqldump -u YOUR_USER -p --databases YOUR_DATABASE > complete_backup.sql

-- 4. Export individual tables (if needed for large datasets)
-- Run these commands in terminal:

-- Export users table
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE users > users_data.sql

-- Export cases table
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE cases > cases_data.sql

-- Export followups table
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE followups > followups_data.sql

-- Export tasks table
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE tasks > tasks_data.sql

-- Export documents table
-- mysqldump -u YOUR_USER -p --no-create-info --no-create-db --no-create-table YOUR_DATABASE documents > documents_data.sql

-- 5. Export to CSV format (for large tables)
-- Run these commands in terminal:

-- Export users to CSV
-- mysql -u YOUR_USER -p -e "SELECT * FROM users" YOUR_DATABASE > users.csv

-- Export cases to CSV
-- mysql -u YOUR_USER -p -e "SELECT * FROM cases" YOUR_DATABASE > cases.csv

-- Export followups to CSV
-- mysql -u YOUR_USER -p -e "SELECT * FROM followups" YOUR_DATABASE > followups.csv

-- Export tasks to CSV
-- mysql -u YOUR_USER -p -e "SELECT * FROM tasks" YOUR_DATABASE > tasks.csv

-- Export documents to CSV
-- mysql -u YOUR_USER -p -e "SELECT * FROM documents" YOUR_DATABASE > documents.csv

-- 6. Verify data integrity before export
-- Run these queries to check data integrity:

-- Check for any NULL values in required fields
SELECT 'users' as table_name, COUNT(*) as null_count 
FROM users WHERE username IS NULL OR name IS NULL OR email IS NULL OR hashed_password IS NULL
UNION ALL
SELECT 'cases', COUNT(*) FROM cases WHERE title IS NULL
UNION ALL
SELECT 'followups', COUNT(*) FROM followups WHERE suggestion_text IS NULL
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks WHERE title IS NULL OR task_type IS NULL OR due_date IS NULL OR created_at IS NULL
UNION ALL
SELECT 'documents', COUNT(*) FROM documents WHERE filename IS NULL OR file_type IS NULL OR content IS NULL OR uploaded_at IS NULL;

-- Check for orphaned records (foreign key integrity)
SELECT 'followups' as table_name, COUNT(*) as orphaned_count 
FROM followups f LEFT JOIN cases c ON f.case_id = c.id WHERE c.id IS NULL
UNION ALL
SELECT 'followups', COUNT(*) FROM followups f LEFT JOIN users u ON f.assigned_to = u.id WHERE f.assigned_to IS NOT NULL AND u.id IS NULL
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks t LEFT JOIN users u ON t.assigned_to = u.id WHERE t.assigned_to IS NOT NULL AND u.id IS NULL
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks t LEFT JOIN users u ON t.assigned_by = u.id WHERE u.id IS NULL
UNION ALL
SELECT 'documents', COUNT(*) FROM documents d LEFT JOIN users u ON d.uploaded_by = u.id WHERE u.id IS NULL;

-- 7. Backup verification
-- After running the export commands, verify the backup files:
-- - Check file sizes are reasonable
-- - Verify file timestamps
-- - Test importing to a test database if possible
