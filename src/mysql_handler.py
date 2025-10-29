"""
MySQL Handler - Enhanced MySQL operations for Hadoop
Author: devnolife
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import csv
import os
from datetime import datetime


class MySQLHandler:
    """Enhanced MySQL handler with better error handling and features"""
    
    def __init__(self, host='localhost', user='root', password='', database=None):
        """Initialize MySQL connection"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish MySQL connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✅ Connected to MySQL database: {self.database or 'None'}")
            return True
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close MySQL connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ MySQL connection closed")
    
    def get_databases(self):
        """Get list of all databases"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute("SHOW DATABASES")
            databases = [db['Database'] for db in self.cursor.fetchall()]
            return databases
        except Error as e:
            print(f"❌ Error getting databases: {e}")
            return []
    
    def get_tables(self):
        """Get list of tables in current database"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute("SHOW TABLES")
            tables = [list(table.values())[0] for table in self.cursor.fetchall()]
            return tables
        except Error as e:
            print(f"❌ Error getting tables: {e}")
            return []
    
    def get_table_info(self, table_name):
        """Get table structure information"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            self.cursor.execute(f"DESCRIBE {table_name}")
            columns = self.cursor.fetchall()
            
            # Get row count
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            row_count = self.cursor.fetchone()['count']
            
            return {
                'columns': columns,
                'row_count': row_count
            }
        except Error as e:
            print(f"❌ Error getting table info: {e}")
            return None
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"❌ Error executing query: {e}")
            return []
    
    def export_table_to_csv(self, table_name, output_file=None, limit=None):
        """Export table to CSV file"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Default output file
            if not output_file:
                output_file = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Build query
            query = f"SELECT * FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
            
            # Execute query
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print(f"⚠️ No data found in table: {table_name}")
                return None
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            print(f"✅ Exported {len(results)} rows to: {output_file}")
            return output_file
        
        except Error as e:
            print(f"❌ Error exporting table: {e}")
            return None
    
    def export_query_to_csv(self, query, output_file=None):
        """Export query results to CSV file"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Default output file
            if not output_file:
                output_file = f"query_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Execute query
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if not results:
                print(f"⚠️ Query returned no results")
                return None
            
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            
            print(f"✅ Exported {len(results)} rows to: {output_file}")
            return output_file
        
        except Error as e:
            print(f"❌ Error exporting query: {e}")
            return None
    
    def get_table_preview(self, table_name, limit=10):
        """Get preview of table data"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            return results
        except Error as e:
            print(f"❌ Error getting table preview: {e}")
            return []
    
    def import_csv_to_table(self, csv_file, table_name, create_table=True):
        """Import CSV file to MySQL table"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Create table if needed
            if create_table:
                # Drop existing table
                self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                
                # Create table structure
                columns = []
                for col in df.columns:
                    # Simple type inference
                    col_type = "VARCHAR(255)"
                    if df[col].dtype in ['int64', 'int32']:
                        col_type = "INT"
                    elif df[col].dtype in ['float64', 'float32']:
                        col_type = "FLOAT"
                    
                    columns.append(f"`{col}` {col_type}")
                
                create_query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
                self.cursor.execute(create_query)
                print(f"✅ Created table: {table_name}")
            
            # Insert data
            placeholders = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
            
            for _, row in df.iterrows():
                self.cursor.execute(insert_query, tuple(row))
            
            self.connection.commit()
            print(f"✅ Imported {len(df)} rows to table: {table_name}")
            return True
            
        except Error as e:
            print(f"❌ Error importing CSV: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Initialize MySQL handler
    mysql = MySQLHandler(
        host='localhost',
        user='root',
        password='your_password',
        database='test_db'
    )
    
    # Connect
    if mysql.connect():
        # Get databases
        print("\n📋 Available Databases:")
        databases = mysql.get_databases()
        for db in databases:
            print(f"  - {db}")
        
        # Get tables
        print("\n📋 Tables in current database:")
        tables = mysql.get_tables()
        for table in tables:
            print(f"  - {table}")
        
        # Export table to CSV
        if tables:
            csv_file = mysql.export_table_to_csv(tables[0], limit=100)
            print(f"\n✅ Exported to: {csv_file}")
        
        # Disconnect
        mysql.disconnect()
