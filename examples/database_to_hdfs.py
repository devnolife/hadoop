"""
Bulk Export MySQL Database to HDFS
Export semua tabel dari MySQL ke HDFS
Author: devnolife
"""

from src.mysql_handler import MySQLHandler
from src.hdfs_operations import HDFSOperations
import os
from datetime import datetime


def export_database_to_hdfs():
    """Export all tables from MySQL to HDFS"""
    
    print("=" * 60)
    print("🔄 MySQL Database to HDFS Exporter")
    print("=" * 60)
    
    # MySQL Configuration
    print("\n📊 MySQL Connection Settings:")
    host = input("Host (localhost): ").strip() or "localhost"
    port = input("Port (3306): ").strip() or "3306"
    user = input("User (root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database name: ").strip()
    
    # HDFS Configuration
    print("\n📁 HDFS Settings:")
    hdfs_base_path = input("HDFS base path (/user/data/mysql): ").strip() or "/user/data/mysql"
    
    try:
        # Connect to MySQL
        print("\n🔌 Connecting to MySQL...")
        mysql = MySQLHandler(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )
        
        if not mysql.connect():
            print("❌ Failed to connect to MySQL")
            return
        
        # Initialize HDFS
        print("🔌 Initializing HDFS operations...")
        hdfs = HDFSOperations()
        
        # Get all tables
        print("\n📋 Fetching tables...")
        tables = mysql.get_tables()
        
        if not tables:
            print("❌ No tables found in database")
            mysql.disconnect()
            return
        
        print(f"✅ Found {len(tables)} tables")
        print("\nTables to export:")
        for i, table in enumerate(tables, 1):
            print(f"  {i}. {table}")
        
        # Confirm export
        confirm = input("\n⚠️  Continue with export? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Export cancelled")
            mysql.disconnect()
            return
        
        # Create exports directory
        os.makedirs('exports', exist_ok=True)
        
        # Export each table
        print("\n" + "=" * 60)
        print("🚀 Starting export process...")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for i, table in enumerate(tables, 1):
            print(f"\n[{i}/{len(tables)}] Processing table: {table}")
            
            try:
                # Export to CSV
                csv_file = f'exports/{table}.csv'
                print(f"  📤 Exporting to CSV: {csv_file}")
                
                row_count = mysql.export_table_to_csv(table, csv_file)
                
                if row_count == 0:
                    print(f"  ⚠️  Table {table} is empty, skipping HDFS upload")
                    continue
                
                print(f"  ✅ Exported {row_count} rows")
                
                # Upload to HDFS
                hdfs_path = f"{hdfs_base_path}/{table}.csv"
                print(f"  📤 Uploading to HDFS: {hdfs_path}")
                
                if hdfs.put_file(csv_file, hdfs_path):
                    print(f"  ✅ Successfully uploaded to HDFS")
                    successful += 1
                else:
                    print(f"  ❌ Failed to upload to HDFS")
                    failed += 1
                
            except Exception as e:
                print(f"  ❌ Error processing {table}: {str(e)}")
                failed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Export Summary")
        print("=" * 60)
        print(f"✅ Successful: {successful} tables")
        print(f"❌ Failed: {failed} tables")
        print(f"📁 Total tables: {len(tables)}")
        print(f"📂 Local exports: ./exports/")
        print(f"☁️  HDFS location: {hdfs_base_path}/")
        
        # Verify HDFS
        print("\n🔍 Verifying HDFS uploads...")
        print(f"Run: hdfs dfs -ls -h {hdfs_base_path}/")
        
        # Disconnect
        mysql.disconnect()
        print("\n✅ Export process completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


def verify_hdfs_uploads(hdfs_path):
    """Verify uploaded files in HDFS"""
    print("\n" + "=" * 60)
    print("🔍 HDFS Verification Commands")
    print("=" * 60)
    print(f"\n# List files")
    print(f"hdfs dfs -ls -h {hdfs_path}/")
    print(f"\n# Check total size")
    print(f"hdfs dfs -du -h {hdfs_path}/")
    print(f"\n# View file content (first 10 lines)")
    print(f"hdfs dfs -cat {hdfs_path}/tablename.csv | head -10")
    print(f"\n# Count rows")
    print(f"hdfs dfs -cat {hdfs_path}/tablename.csv | wc -l")


if __name__ == "__main__":
    try:
        export_database_to_hdfs()
        
        print("\n" + "=" * 60)
        hdfs_path = input("\nShow verification commands? (y/n): ").strip().lower()
        if hdfs_path == 'y':
            verify_hdfs_uploads("/user/data/mysql")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Export interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
