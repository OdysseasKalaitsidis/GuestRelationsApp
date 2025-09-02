-- Migration Verification Script
-- Run this after completing the migration to verify everything is working correctly

-- 1. Verify all tables exist
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'cases', 'followups', 'tasks', 'documents')
ORDER BY table_name;

-- 2. Verify table structures match expectations
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default,
    ordinal_position
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'cases', 'followups', 'tasks', 'documents')
ORDER BY table_name, ordinal_position;

-- 3. Verify indexes are created
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename IN ('users', 'cases', 'followups', 'tasks', 'documents')
AND indexname NOT LIKE '%_pkey'  -- Exclude primary key indexes
ORDER BY tablename, indexname;

-- 4. Verify foreign key constraints
SELECT 
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    tc.constraint_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public'
AND tc.table_name IN ('users', 'cases', 'followups', 'tasks', 'documents')
ORDER BY tc.table_name, kcu.column_name;

-- 5. Verify sequences (AUTO_INCREMENT equivalents)
SELECT 
    sequence_name,
    data_type,
    start_value,
    minimum_value,
    maximum_value,
    increment
FROM information_schema.sequences 
WHERE sequence_schema = 'public'
AND sequence_name IN (
    'users_id_seq',
    'cases_id_seq', 
    'followups_id_seq',
    'tasks_id_seq',
    'documents_id_seq'
)
ORDER BY sequence_name;

-- 6. Verify triggers
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_statement
FROM information_schema.triggers 
WHERE trigger_schema = 'public'
AND event_object_table IN ('users', 'cases', 'followups', 'tasks', 'documents')
ORDER BY event_object_table, trigger_name;

-- 7. Verify extensions are enabled
SELECT 
    extname,
    extversion
FROM pg_extension 
WHERE extname IN ('pgcrypto', 'pg_trgm', 'uuid-ossp');

-- 8. Test data insertion (if tables are empty)
-- Uncomment and run these if you want to test with sample data

-- INSERT INTO users (username, name, email, hashed_password, is_admin) 
-- VALUES ('testuser', 'Test User', 'test@example.com', 'hashed_password', false)
-- ON CONFLICT (username) DO NOTHING;

-- INSERT INTO cases (title, status, owner_id) 
-- VALUES ('Test Case', 'open', 1)
-- ON CONFLICT DO NOTHING;

-- 9. Verify row counts (compare with MySQL)
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'cases', COUNT(*) FROM cases
UNION ALL
SELECT 'followups', COUNT(*) FROM followups
UNION ALL
SELECT 'tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'documents', COUNT(*) FROM documents
ORDER BY table_name;

-- 10. Test foreign key relationships
-- This should return 0 if all relationships are intact
SELECT 'orphaned_followups' as issue, COUNT(*) as count
FROM followups f 
LEFT JOIN cases c ON f.case_id = c.id 
WHERE c.id IS NULL
UNION ALL
SELECT 'orphaned_tasks_assigned', COUNT(*)
FROM tasks t 
LEFT JOIN users u ON t.assigned_to = u.id 
WHERE t.assigned_to IS NOT NULL AND u.id IS NULL
UNION ALL
SELECT 'orphaned_tasks_assigner', COUNT(*)
FROM tasks t 
LEFT JOIN users u ON t.assigned_by = u.id 
WHERE u.id IS NULL
UNION ALL
SELECT 'orphaned_documents', COUNT(*)
FROM documents d 
LEFT JOIN users u ON d.uploaded_by = u.id 
WHERE u.id IS NULL;

-- 11. Test basic CRUD operations
-- Uncomment to test basic operations

-- -- Test SELECT
-- SELECT * FROM users LIMIT 5;
-- SELECT * FROM cases LIMIT 5;

-- -- Test UPDATE (if you have data)
-- -- UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = 1;

-- -- Test DELETE (be careful!)
-- -- DELETE FROM users WHERE username = 'testuser';

-- 12. Performance check
-- Check if indexes are being used
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE username = 'testuser';
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM cases WHERE owner_id = 1;
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM followups WHERE case_id = 1;

-- 13. Connection test
-- This should return 1 if connection is working
SELECT 1 as connection_test;

-- 14. Final verification summary
SELECT 
    'Schema Migration Complete' as status,
    COUNT(*) as tables_created
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('users', 'cases', 'followups', 'tasks', 'documents')
HAVING COUNT(*) = 5;
