#!/usr/bin/env python3
"""
Reset database completely - drop all tables and recreate them
"""

from db import engine
from models import Base
from sqlalchemy import text

def reset_database():
    """Drop all tables and recreate them"""
    try:
        # Drop all tables
        with engine.connect() as conn:
            # Disable foreign key checks temporarily
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Get all table names
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            print(f"Found tables: {tables}")
            
            # Drop all tables
            for table in tables:
                print(f"Dropping table: {table}")
                conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
            
            # Re-enable foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
            conn.commit()
            print("✅ All tables dropped")
        
        # Recreate all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables recreated successfully")
        
        # Verify table structure
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print(f"New tables: {tables}")
            
            # Check cases table structure
            if 'cases' in tables:
                result = conn.execute(text("DESCRIBE cases"))
                columns = [row[0] for row in result]
                print(f"Cases table columns: {columns}")
            
    except Exception as e:
        print(f"❌ Error resetting database: {e}")

if __name__ == "__main__":
    reset_database() 