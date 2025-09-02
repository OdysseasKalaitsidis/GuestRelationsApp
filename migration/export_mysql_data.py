#!/usr/bin/env python3
"""
MySQL to Supabase Migration Script
Exports data from MySQL and prepares for Supabase import
"""

import mysql.connector
import json
import csv
import os
from datetime import datetime

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'myuser',
    'password': 'Odkalaitsidis12@',
    'database': 'mydb',
    'port': 3306
}

# Supabase Configuration
SUPABASE_CONFIG = {
    'host': 'db.sjjuaesddqzfcdahutfl.supabase.co',
    'user': 'postgres',
    'password': 'Odysseaskal',
    'database': 'postgres',
    'port': 5432
}

def connect_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print("✅ Connected to MySQL database successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to MySQL: {err}")
        return None

def get_table_info(connection):
    """Get information about all tables"""
    cursor = connection.cursor()
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
    
    # Get table details
    table_info = {}
    for table in tables:
        cursor.execute(f"DESCRIBE {table}")
        columns = cursor.fetchall()
        table_info[table] = columns
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]
        print(f"  - {table}: {row_count} rows")
    
    cursor.close()
    return table_info

def export_table_data(connection, table_name, output_dir):
    """Export table data to CSV"""
    cursor = connection.cursor()
    
    # Get all data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [col[0] for col in cursor.fetchall()]
    
    # Write to CSV
    csv_file = os.path.join(output_dir, f"{table_name}.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)
    
    print(f"📄 Exported {len(rows)} rows from {table_name} to {csv_file}")
    cursor.close()
    return len(rows)

def export_schema(connection, output_dir):
    """Export database schema"""
    cursor = connection.cursor()
    
    # Get all tables
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    schema_file = os.path.join(output_dir, "schema.sql")
    with open(schema_file, 'w', encoding='utf-8') as file:
        for table in tables:
            # Get CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE {table}")
            create_statement = cursor.fetchone()[1]
            file.write(f"{create_statement};\n\n")
    
    print(f"📋 Exported schema to {schema_file}")
    cursor.close()

def main():
    """Main migration function"""
    print("🚀 Starting MySQL to Supabase Migration")
    print("=" * 50)
    
    # Create output directory
    output_dir = "migration/backups"
    os.makedirs(output_dir, exist_ok=True)
    
    # Connect to MySQL
    connection = connect_mysql()
    if not connection:
        return
    
    try:
        # Get table information
        table_info = get_table_info(connection)
        
        # Export schema
        export_schema(connection, output_dir)
        
        # Export data for each table
        total_rows = 0
        for table in table_info.keys():
            if table in ['users', 'cases', 'followups', 'tasks', 'documents']:
                rows = export_table_data(connection, table, output_dir)
                total_rows += rows
        
        print(f"\n✅ Migration export completed!")
        print(f"📊 Total rows exported: {total_rows}")
        print(f"📁 Files saved in: {output_dir}")
        
        # Create migration summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'tables_exported': list(table_info.keys()),
            'total_rows': total_rows,
            'mysql_config': MYSQL_CONFIG,
            'supabase_config': SUPABASE_CONFIG
        }
        
        with open(os.path.join(output_dir, 'migration_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Migration summary saved to: {output_dir}/migration_summary.json")
        
    finally:
        connection.close()
        print("🔌 MySQL connection closed")

if __name__ == "__main__":
    main()
