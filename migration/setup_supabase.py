#!/usr/bin/env python3
"""
Supabase Setup and Data Import Script
Sets up Supabase schema and imports MySQL data
"""

import psycopg2
import csv
import json
import os
from datetime import datetime

# Supabase Configuration
SUPABASE_CONFIG = {
    'host': 'db.sjjuaesddqzfcdahutfl.supabase.co',
    'user': 'postgres',
    'password': 'Odysseaskal',
    'database': 'postgres',
    'port': 5432,
    'sslmode': 'require'
}

def connect_supabase():
    """Connect to Supabase PostgreSQL"""
    try:
        connection = psycopg2.connect(**SUPABASE_CONFIG)
        print("✅ Connected to Supabase PostgreSQL successfully")
        return connection
    except psycopg2.Error as err:
        print(f"❌ Error connecting to Supabase: {err}")
        return None

def setup_supabase_schema(connection):
    """Set up Supabase schema with tables"""
    cursor = connection.cursor()
    
    # Enable extensions
    extensions = [
        "CREATE EXTENSION IF NOT EXISTS pgcrypto;",
        "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
        "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
    ]
    
    for ext in extensions:
        cursor.execute(ext)
    
    # Create tables
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS cases (
            id SERIAL PRIMARY KEY,
            room VARCHAR(50),
            status VARCHAR(50),
            importance VARCHAR(50),
            type VARCHAR(50),
            title TEXT,
            action TEXT,
            owner_id INTEGER REFERENCES users(id),
            guest VARCHAR(255),
            created VARCHAR(100),
            created_by VARCHAR(255),
            modified VARCHAR(100),
            modified_by VARCHAR(255),
            source VARCHAR(255),
            membership VARCHAR(255),
            case_description TEXT,
            in_out VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS followups (
            id SERIAL PRIMARY KEY,
            case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
            suggestion_text TEXT NOT NULL,
            assigned_to INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            task_type VARCHAR(50) NOT NULL,
            assigned_to INTEGER REFERENCES users(id),
            assigned_by INTEGER REFERENCES users(id) NOT NULL,
            due_date VARCHAR(50) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at VARCHAR(50) NOT NULL,
            completed_at VARCHAR(50),
            created_at_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            uploaded_by INTEGER REFERENCES users(id) NOT NULL,
            uploaded_at VARCHAR(50) NOT NULL,
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    for table_sql in tables_sql:
        cursor.execute(table_sql)
    
    # Create indexes
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_cases_owner_id ON cases(owner_id);",
        "CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);",
        "CREATE INDEX IF NOT EXISTS idx_followups_case_id ON followups(case_id);",
        "CREATE INDEX IF NOT EXISTS idx_followups_assigned_to ON followups(assigned_to);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_assigned_by ON tasks(assigned_by);",
        "CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);",
        "CREATE INDEX IF NOT EXISTS idx_documents_uploaded_by ON documents(uploaded_by);",
        "CREATE INDEX IF NOT EXISTS idx_documents_file_type ON documents(file_type);"
    ]
    
    for index in indexes:
        cursor.execute(index)
    
    # Create updated_at trigger function
    trigger_function = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    cursor.execute(trigger_function)
    
    # Create triggers
    triggers = [
        "CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_cases_updated_at BEFORE UPDATE ON cases FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_followups_updated_at BEFORE UPDATE ON followups FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();",
        "CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();"
    ]
    
    for trigger in triggers:
        cursor.execute(trigger)
    
    connection.commit()
    cursor.close()
    print("✅ Supabase schema setup completed")

def import_csv_data(connection, csv_file, table_name):
    """Import CSV data to Supabase table"""
    cursor = connection.cursor()
    
    csv_path = os.path.join("migration/backups", csv_file)
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        # Build INSERT statement
        columns = ', '.join(headers)
        placeholders = ', '.join(['%s'] * len(headers))
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Insert data
        rows_imported = 0
        for row in reader:
            try:
                cursor.execute(insert_sql, row)
                rows_imported += 1
            except Exception as e:
                print(f"⚠️ Error importing row {rows_imported + 1}: {e}")
                continue
        
        connection.commit()
        print(f"📄 Imported {rows_imported} rows to {table_name}")
        cursor.close()
        return rows_imported

def main():
    """Main setup and import function"""
    print("🚀 Setting up Supabase and importing data")
    print("=" * 50)
    
    # Connect to Supabase
    connection = connect_supabase()
    if not connection:
        return
    
    try:
        # Setup schema
        setup_supabase_schema(connection)
        
        # Import data
        total_imported = 0
        import_mapping = [
            ("users.csv", "users"),
            ("cases.csv", "cases"),
            ("followups.csv", "followups"),
            ("tasks.csv", "tasks"),
            ("documents.csv", "documents")
        ]
        
        for csv_file, table_name in import_mapping:
            rows = import_csv_data(connection, csv_file, table_name)
            total_imported += rows
        
        print(f"\n✅ Data import completed!")
        print(f"📊 Total rows imported: {total_imported}")
        
        # Fix sequences
        cursor = connection.cursor()
        sequences = [
            ("users", "id"),
            ("cases", "id"),
            ("followups", "id"),
            ("tasks", "id"),
            ("documents", "id")
        ]
        
        for table, column in sequences:
            try:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table}', '{column}'), (SELECT MAX({column}) FROM {table}));")
                print(f"✅ Fixed sequence for {table}")
            except Exception as e:
                print(f"⚠️ Could not fix sequence for {table}: {e}")
        
        connection.commit()
        cursor.close()
        
        print(f"\n🎉 Supabase migration completed successfully!")
        
    finally:
        connection.close()
        print("🔌 Supabase connection closed")

if __name__ == "__main__":
    main()
