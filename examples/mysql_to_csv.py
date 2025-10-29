"""
MySQL to CSV Export - Simple Example
Author: devnolife
"""

from src.mysql_handler import MySQLHandler


def main():
    print("="*60)
    print("MySQL to CSV Export Tool")
    print("Created by devnolife")
    print("="*60)
    
    # Get user input
    print("\n📋 MySQL Connection Details:")
    host = input("Host [localhost]: ").strip() or 'localhost'
    user = input("User [root]: ").strip() or 'root'
    password = input("Password: ").strip()
    database = input("Database: ").strip()
    
    # Connect to MySQL
    print(f"\n🔌 Connecting to MySQL...")
    mysql = MySQLHandler(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    if not mysql.connect():
        print("❌ Connection failed!")
        return
    
    # Get tables
    print("\n📋 Available Tables:")
    tables = mysql.get_tables()
    
    if not tables:
        print("⚠️ No tables found in database")
        mysql.disconnect()
        return
    
    for i, table in enumerate(tables, 1):
        info = mysql.get_table_info(table)
        rows = info['row_count'] if info else 'N/A'
        cols = len(info['columns']) if info else 'N/A'
        print(f"{i}. {table} ({rows} rows, {cols} columns)")
    
    # Select table
    print("\nSelect table to export:")
    choice = input("Enter number (or 'all' for all tables): ").strip()
    
    if choice.lower() == 'all':
        # Export all tables
        print("\n📥 Exporting all tables...")
        for table in tables:
            print(f"\nExporting: {table}")
            csv_file = mysql.export_table_to_csv(table)
            if csv_file:
                print(f"✅ Saved to: {csv_file}")
    else:
        # Export selected table
        try:
            index = int(choice) - 1
            if 0 <= index < len(tables):
                table = tables[index]
                
                # Ask for limit
                limit_input = input(f"\nLimit rows (press Enter for all): ").strip()
                limit = int(limit_input) if limit_input else None
                
                print(f"\n📥 Exporting: {table}")
                csv_file = mysql.export_table_to_csv(table, limit=limit)
                
                if csv_file:
                    print(f"✅ Saved to: {csv_file}")
                    
                    # Preview
                    preview = input("\nPreview data? (y/n): ").strip().lower()
                    if preview == 'y':
                        data = mysql.get_table_preview(table, limit=5)
                        print("\n📊 Preview (first 5 rows):")
                        for row in data:
                            print(row)
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Invalid input")
    
    # Disconnect
    mysql.disconnect()
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
