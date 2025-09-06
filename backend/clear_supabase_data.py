#!/usr/bin/env python3
"""
Script to delete all data from Supabase database
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from supabase_client import initialize_supabase, get_supabase

async def clear_all_supabase_data():
    """Clear all data from Supabase database"""
    print("🗑️ Clearing all data from Supabase database...")
    print("=" * 60)
    
    # Initialize Supabase
    if not initialize_supabase():
        print("❌ Failed to initialize Supabase")
        return False
    
    print("✅ Supabase initialized successfully")
    
    try:
        supabase = get_supabase()
        
        # List of tables to clear (in order to respect foreign key constraints)
        tables_to_clear = [
            "followups",  # Clear followups first (has foreign keys)
            "documents",  # Clear documents second
            "cases",      # Clear cases third
            "users"       # Clear users last (other tables reference users)
        ]
        
        for table in tables_to_clear:
            print(f"\n🗑️ Clearing {table} table...")
            
            # First, get count of records
            count_response = supabase.table(table).select("id", count="exact").execute()
            record_count = count_response.count if hasattr(count_response, 'count') else 0
            
            if record_count > 0:
                print(f"   Found {record_count} records in {table}")
                
                # Delete all records
                delete_response = supabase.table(table).delete().neq("id", 0).execute()
                
                if delete_response.data is not None:
                    print(f"   ✅ Successfully deleted all records from {table}")
                else:
                    print(f"   ❌ Failed to delete records from {table}")
                    if hasattr(delete_response, 'error'):
                        print(f"   Error: {delete_response.error}")
            else:
                print(f"   ℹ️ No records found in {table}")
        
        print("\n" + "=" * 60)
        print("🎉 Database clearing completed!")
        
        # Verify all tables are empty
        print("\n📊 Verification - Checking remaining records:")
        for table in tables_to_clear:
            count_response = supabase.table(table).select("id", count="exact").execute()
            record_count = count_response.count if hasattr(count_response, 'count') else 0
            print(f"   {table}: {record_count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(clear_all_supabase_data())
    if success:
        print("\n✅ All data has been successfully deleted from Supabase!")
    else:
        print("\n❌ Failed to delete data from Supabase!")
