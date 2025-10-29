"""
Backup Database to CSV - Complete Example
Author: devnolife
"""

from src.mysql_handler import MySQLHandler
import os
from datetime import datetime


def backup_database(host, user, password, database, output_dir='backups'):
    """
    Backup all tables in a database to CSV files
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamp for backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(output_dir, f"{database}_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    
    print(f"🗄️ Starting backup for database: {database}")
    print(f"📁 Backup location: {backup_folder}\n")
    
    # Connect to MySQL
    mysql = MySQLHandler(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    if not mysql.connect():
        print("❌ Failed to connect to MySQL")
        return
    
    # Get all tables
    tables = mysql.get_tables()
    print(f"📋 Found {len(tables)} tables\n")
    
    # Export each table
    total_rows = 0
    for i, table in enumerate(tables, 1):
        print(f"[{i}/{len(tables)}] Exporting: {table}")
        
        # Get table info
        info = mysql.get_table_info(table)
        if info:
            print(f"  ├─ Rows: {info['row_count']:,}")
            print(f"  ├─ Columns: {len(info['columns'])}")
            total_rows += info['row_count']
        
        # Export to CSV
        output_file = os.path.join(backup_folder, f"{table}.csv")
        csv_file = mysql.export_table_to_csv(table, output_file)
        
        if csv_file:
            file_size = os.path.getsize(csv_file)
            print(f"  └─ ✅ Exported ({file_size:,} bytes)\n")
        else:
            print(f"  └─ ❌ Failed to export\n")
    
    # Summary
    print("="*60)
    print("📊 Backup Summary:")
    print(f"  Database: {database}")
    print(f"  Tables: {len(tables)}")
    print(f"  Total Rows: {total_rows:,}")
    print(f"  Location: {backup_folder}")
    print("="*60)
    
    # Disconnect
    mysql.disconnect()
    
    return backup_folder


def restore_from_csv(host, user, password, database, backup_folder):
    """
    Restore database from CSV backup
    """
    print(f"🔄 Restoring database: {database}")
    print(f"📁 From backup: {backup_folder}\n")
    
    # Connect to MySQL
    mysql = MySQLHandler(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    if not mysql.connect():
        print("❌ Failed to connect to MySQL")
        return
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(backup_folder) if f.endswith('.csv')]
    print(f"📋 Found {len(csv_files)} CSV files\n")
    
    # Import each CSV
    for i, csv_file in enumerate(csv_files, 1):
        table_name = os.path.splitext(csv_file)[0]
        csv_path = os.path.join(backup_folder, csv_file)
        
        print(f"[{i}/{len(csv_files)}] Importing: {table_name}")
        
        success = mysql.import_csv_to_table(csv_path, table_name, create_table=True)
        
        if success:
            print(f"  └─ ✅ Imported\n")
        else:
            print(f"  └─ ❌ Failed\n")
    
    print("="*60)
    print("✅ Restore completed!")
    print("="*60)
    
    # Disconnect
    mysql.disconnect()


# Example usage
if __name__ == "__main__":
    # Configuration
    MYSQL_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'your_password',  # Change this!
        'database': 'test_db'
    }
    
    # Backup database
    backup_folder = backup_database(**MYSQL_CONFIG)
    
    # Optional: Restore from backup
    # restore_from_csv(**MYSQL_CONFIG, backup_folder=backup_folder)
