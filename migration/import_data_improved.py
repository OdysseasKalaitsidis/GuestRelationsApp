#!/usr/bin/env python3
"""
Improved Supabase Data Import Script
Handles data type conversions and CSV parsing issues
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

def clean_value(value):
    """Clean and convert values for PostgreSQL"""
    if value is None or value == '':
        return None
    
    # Remove extra whitespace and newlines
    value = str(value).strip().replace('\n', ' ').replace('\r', ' ')
    
    # Handle boolean conversion
    if value.lower() in ['1', 'true', 'yes']:
        return True
    elif value.lower() in ['0', 'false', 'no']:
        return False
    
    return value

def import_users(connection):
    """Import users table with proper data handling"""
    cursor = connection.cursor()
    
    csv_path = os.path.join("migration/backups", "users.csv")
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    # Read the entire file and clean it
    with open(csv_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Remove line breaks within quoted fields
        lines = content.split('\n')
        cleaned_lines = []
        current_line = ""
        
        for line in lines:
            if line.count(',') >= 5:  # Complete line
                if current_line:
                    current_line += " " + line
                    cleaned_lines.append(current_line)
                    current_line = ""
                else:
                    cleaned_lines.append(line)
            else:
                current_line += " " + line if current_line else line
    
    # Parse the cleaned data
    rows_imported = 0
    for i, line in enumerate(cleaned_lines):
        if i == 0:  # Skip header
            continue
        
        try:
            # Split by comma, but handle quoted fields
            parts = line.split(',')
            if len(parts) >= 6:
                user_id = int(parts[0]) if parts[0].strip() else None
                username = clean_value(parts[1])
                name = clean_value(parts[2])
                email = clean_value(parts[3])
                hashed_password = clean_value(parts[4])
                is_admin = clean_value(parts[5])
                
                # Convert is_admin to boolean
                is_admin_bool = False
                if is_admin:
                    is_admin_bool = str(is_admin).lower() in ['1', 'true', 'yes']
                
                # Insert with proper data types
                insert_sql = """
                INSERT INTO users (id, username, name, email, hashed_password, is_admin)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                username = EXCLUDED.username,
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                hashed_password = EXCLUDED.hashed_password,
                is_admin = EXCLUDED.is_admin;
                """
                
                cursor.execute(insert_sql, (user_id, username, name, email, hashed_password, is_admin_bool))
                rows_imported += 1
                print(f"✅ Imported user: {username}")
                
        except Exception as e:
            print(f"⚠️ Error importing user row {i}: {e}")
            continue
    
    connection.commit()
    cursor.close()
    print(f"📄 Imported {rows_imported} users")
    return rows_imported

def import_cases(connection):
    """Import cases table"""
    cursor = connection.cursor()
    
    csv_path = os.path.join("migration/backups", "cases.csv")
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        rows_imported = 0
        for row in reader:
            try:
                # Clean and convert values
                cleaned_row = [clean_value(val) for val in row]
                
                # Handle owner_id conversion
                if cleaned_row[7] and cleaned_row[7].isdigit():  # owner_id
                    cleaned_row[7] = int(cleaned_row[7])
                else:
                    cleaned_row[7] = None
                
                # Build INSERT statement
                columns = ', '.join(headers)
                placeholders = ', '.join(['%s'] * len(headers))
                insert_sql = f"INSERT INTO cases ({columns}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING;"
                
                cursor.execute(insert_sql, cleaned_row)
                rows_imported += 1
                
            except Exception as e:
                print(f"⚠️ Error importing case row {rows_imported + 1}: {e}")
                continue
    
    connection.commit()
    cursor.close()
    print(f"📄 Imported {rows_imported} cases")
    return rows_imported

def import_followups(connection):
    """Import followups table"""
    cursor = connection.cursor()
    
    csv_path = os.path.join("migration/backups", "followups.csv")
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found: {csv_path}")
        return 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        rows_imported = 0
        for row in reader:
            try:
                # Clean and convert values
                cleaned_row = [clean_value(val) for val in row]
                
                # Handle foreign key conversions
                if cleaned_row[1] and cleaned_row[1].isdigit():  # case_id
                    cleaned_row[1] = int(cleaned_row[1])
                else:
                    cleaned_row[1] = None
                
                if cleaned_row[3] and cleaned_row[3].isdigit():  # assigned_to
                    cleaned_row[3] = int(cleaned_row[3])
                else:
                    cleaned_row[3] = None
                
                # Build INSERT statement
                columns = ', '.join(headers)
                placeholders = ', '.join(['%s'] * len(headers))
                insert_sql = f"INSERT INTO followups ({columns}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING;"
                
                cursor.execute(insert_sql, cleaned_row)
                rows_imported += 1
                
            except Exception as e:
                print(f"⚠️ Error importing followup row {rows_imported + 1}: {e}")
                continue
    
    connection.commit()
    cursor.close()
    print(f"📄 Imported {rows_imported} followups")
    return rows_imported

def main():
    """Main import function"""
    print("🚀 Importing data to Supabase with improved handling")
    print("=" * 50)
    
    # Connect to Supabase
    connection = connect_supabase()
    if not connection:
        return
    
    try:
        total_imported = 0
        
        # Import users first (they're referenced by other tables)
        users_imported = import_users(connection)
        total_imported += users_imported
        
        # Import cases
        cases_imported = import_cases(connection)
        total_imported += cases_imported
        
        # Import followups
        followups_imported = import_followups(connection)
        total_imported += followups_imported
        
        print(f"\n✅ Data import completed!")
        print(f"📊 Total rows imported: {total_imported}")
        print(f"  - Users: {users_imported}")
        print(f"  - Cases: {cases_imported}")
        print(f"  - Followups: {followups_imported}")
        
        # Fix sequences
        cursor = connection.cursor()
        sequences = [
            ("users", "id"),
            ("cases", "id"),
            ("followups", "id")
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
