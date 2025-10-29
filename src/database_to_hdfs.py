"""
Script untuk Memasukkan Data dari Database ke HDFS
Menggunakan Python untuk koneksi database dan transfer ke HDFS
"""

import subprocess
import json
import csv
import os

class DatabaseToHDFS:
    def __init__(self):
        self.hdfs_cmd = "hdfs dfs"
        
    def mysql_to_csv(self, host, user, password, database, table, output_file):
        """Export data dari MySQL ke CSV"""
        print(f"\n=== Export MySQL Table: {table} ===")
        
        try:
            import mysql.connector
            
            # Koneksi ke MySQL
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            
            # Tulis ke CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([i[0] for i in cursor.description])
                # Data
                writer.writerows(cursor.fetchall())
            
            cursor.close()
            conn.close()
            
            print(f"✓ Data berhasil di-export ke {output_file}")
            return True
            
        except ImportError:
            print("✗ mysql-connector-python belum terinstal")
            print("Install dengan: pip install mysql-connector-python")
            return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return False
    
    def postgres_to_csv(self, host, user, password, database, table, output_file):
        """Export data dari PostgreSQL ke CSV"""
        print(f"\n=== Export PostgreSQL Table: {table} ===")
        
        try:
            import psycopg2
            
            # Koneksi ke PostgreSQL
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            
            # Tulis ke CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([desc[0] for desc in cursor.description])
                # Data
                writer.writerows(cursor.fetchall())
            
            cursor.close()
            conn.close()
            
            print(f"✓ Data berhasil di-export ke {output_file}")
            return True
            
        except ImportError:
            print("✗ psycopg2 belum terinstal")
            print("Install dengan: pip install psycopg2-binary")
            return False
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return False
    
    def upload_to_hdfs(self, local_file, hdfs_path):
        """Upload file ke HDFS"""
        print(f"\n=== Upload to HDFS ===")
        print(f"Local: {local_file}")
        print(f"HDFS: {hdfs_path}")
        
        if not os.path.exists(local_file):
            print(f"✗ File tidak ditemukan: {local_file}")
            return False
        
        command = f"{self.hdfs_cmd} -put {local_file} {hdfs_path}"
        
        try:
            result = subprocess.run(command, 
                                  shell=True, 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                print(f"✓ Upload berhasil ke {hdfs_path}")
                return True
            else:
                print(f"✗ Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return False
    
    def mysql_to_hdfs(self, db_config, table, hdfs_path):
        """Pipeline lengkap: MySQL -> CSV -> HDFS"""
        print("=" * 60)
        print("PIPELINE: MySQL -> CSV -> HDFS")
        print("=" * 60)
        
        temp_file = f"temp_{table}.csv"
        
        # Export dari MySQL
        success = self.mysql_to_csv(
            db_config['host'],
            db_config['user'],
            db_config['password'],
            db_config['database'],
            table,
            temp_file
        )
        
        if not success:
            return False
        
        # Upload ke HDFS
        success = self.upload_to_hdfs(temp_file, hdfs_path)
        
        # Hapus file temporary (opsional)
        if success and os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"✓ File temporary dihapus: {temp_file}")
        
        return success
    
    def sqoop_import(self, jdbc_url, username, password, table, target_dir):
        """Import data menggunakan Apache Sqoop"""
        print("\n=== Import Data dengan Sqoop ===")
        
        command = f"""sqoop import \
  --connect {jdbc_url} \
  --username {username} \
  --password {password} \
  --table {table} \
  --target-dir {target_dir} \
  --m 1"""
        
        print(f"Command:\n{command}\n")
        
        try:
            result = subprocess.run(command, 
                                  shell=True, 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                print("✓ Sqoop import berhasil")
                return True
            else:
                print(f"✗ Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return False

def example_usage():
    """Contoh penggunaan"""
    db_to_hdfs = DatabaseToHDFS()
    
    print("=" * 60)
    print("CONTOH: MEMASUKKAN DATA DARI DATABASE KE HDFS")
    print("=" * 60)
    
    # Contoh konfigurasi database
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'mydb'
    }
    
    print("\n--- Metode 1: Python Script ---")
    print("db_to_hdfs.mysql_to_hdfs(")
    print("    db_config=mysql_config,")
    print("    table='customers',")
    print("    hdfs_path='/user/hadoop/data/customers.csv'")
    print(")")
    
    print("\n--- Metode 2: Apache Sqoop ---")
    print("db_to_hdfs.sqoop_import(")
    print("    jdbc_url='jdbc:mysql://localhost:3306/mydb',")
    print("    username='root',")
    print("    password='password',")
    print("    table='customers',")
    print("    target_dir='/user/hadoop/sqoop/customers'")
    print(")")
    
    print("\n" + "=" * 60)
    print("Catatan:")
    print("- Install driver: pip install mysql-connector-python")
    print("- Untuk PostgreSQL: pip install psycopg2-binary")
    print("- Untuk Sqoop: Install Apache Sqoop terpisah")
    print("=" * 60)

if __name__ == "__main__":
    example_usage()
