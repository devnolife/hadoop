"""
Script untuk Operasi HDFS (Hadoop Distributed File System)
Menjalankan Perintah Dasar Hadoop dan Mengambil/Memasukkan Data
"""

import subprocess
import os
import sys

class HDFSOperations:
    def __init__(self):
        self.hdfs_cmd = "hdfs dfs"
        
    def run_command(self, command):
        """Menjalankan command HDFS"""
        try:
            result = subprocess.run(command, 
                                  shell=True, 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                print(f"✓ Success: {command}")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"✗ Error: {command}")
                print(result.stderr)
            return result
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
            return None
    
    def list_directory(self, path="/"):
        """List isi direktori HDFS"""
        print(f"\n=== List Directory: {path} ===")
        command = f"{self.hdfs_cmd} -ls {path}"
        return self.run_command(command)
    
    def create_directory(self, path):
        """Membuat direktori di HDFS"""
        print(f"\n=== Create Directory: {path} ===")
        command = f"{self.hdfs_cmd} -mkdir -p {path}"
        return self.run_command(command)
    
    def upload_file(self, local_path, hdfs_path):
        """Upload file dari local ke HDFS (put)"""
        print(f"\n=== Upload File ===")
        print(f"From: {local_path}")
        print(f"To: {hdfs_path}")
        
        if not os.path.exists(local_path):
            print(f"✗ File tidak ditemukan: {local_path}")
            return None
            
        command = f"{self.hdfs_cmd} -put {local_path} {hdfs_path}"
        return self.run_command(command)
    
    def download_file(self, hdfs_path, local_path):
        """Download file dari HDFS ke local (get)"""
        print(f"\n=== Download File ===")
        print(f"From HDFS: {hdfs_path}")
        print(f"To Local: {local_path}")
        
        command = f"{self.hdfs_cmd} -get {hdfs_path} {local_path}"
        return self.run_command(command)
    
    def cat_file(self, hdfs_path):
        """Menampilkan isi file di HDFS"""
        print(f"\n=== Cat File: {hdfs_path} ===")
        command = f"{self.hdfs_cmd} -cat {hdfs_path}"
        return self.run_command(command)
    
    def remove_file(self, hdfs_path):
        """Menghapus file/direktori di HDFS"""
        print(f"\n=== Remove: {hdfs_path} ===")
        command = f"{self.hdfs_cmd} -rm -r {hdfs_path}"
        return self.run_command(command)
    
    def copy_from_local(self, local_path, hdfs_path):
        """Copy file dari local ke HDFS"""
        print(f"\n=== Copy From Local ===")
        command = f"{self.hdfs_cmd} -copyFromLocal {local_path} {hdfs_path}"
        return self.run_command(command)
    
    def copy_to_local(self, hdfs_path, local_path):
        """Copy file dari HDFS ke local"""
        print(f"\n=== Copy To Local ===")
        command = f"{self.hdfs_cmd} -copyToLocal {hdfs_path} {local_path}"
        return self.run_command(command)
    
    def get_file_info(self, hdfs_path):
        """Mendapatkan informasi file"""
        print(f"\n=== File Info: {hdfs_path} ===")
        command = f"{self.hdfs_cmd} -stat %n,%b,%r,%u,%g {hdfs_path}"
        return self.run_command(command)
    
    def disk_usage(self, path="/"):
        """Melihat disk usage"""
        print(f"\n=== Disk Usage: {path} ===")
        command = f"{self.hdfs_cmd} -du -h {path}"
        return self.run_command(command)
    
    # Wrapper methods for Flask app compatibility
    def put_file(self, local_path, hdfs_path):
        """Wrapper for upload_file - Upload file to HDFS"""
        result = self.upload_file(local_path, hdfs_path)
        return result is not None and result.returncode == 0
    
    def get_file(self, hdfs_path, local_path):
        """Wrapper for download_file - Download file from HDFS"""
        result = self.download_file(hdfs_path, local_path)
        return result is not None and result.returncode == 0

def demo_operations():
    """Demo operasi HDFS"""
    hdfs = HDFSOperations()
    
    print("=" * 60)
    print("DEMO OPERASI HDFS")
    print("=" * 60)
    
    # Membuat direktori
    hdfs.create_directory("/user/hadoop/input")
    hdfs.create_directory("/user/hadoop/output")
    
    # List direktori
    hdfs.list_directory("/user/hadoop")
    
    # Disk usage
    hdfs.disk_usage("/user/hadoop")
    
    print("\n" + "=" * 60)
    print("Untuk upload/download file, gunakan:")
    print("hdfs.upload_file('local_file.txt', '/user/hadoop/input/file.txt')")
    print("hdfs.download_file('/user/hadoop/output/result.txt', 'result.txt')")
    print("=" * 60)

if __name__ == "__main__":
    demo_operations()
