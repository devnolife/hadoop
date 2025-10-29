"""
ALTERNATIF: Simulasi HDFS Operations TANPA Java/Hadoop
Menggunakan Python murni untuk operasi file terdistribusi
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class MockHDFS:
    """
    Simulasi HDFS menggunakan file system lokal
    TIDAK MEMERLUKAN Java atau Hadoop!
    Cocok untuk pembelajaran atau testing
    """
    
    def __init__(self, base_path="./mock_hdfs"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        print(f"✓ Mock HDFS initialized at: {self.base_path.absolute()}")
    
    def _get_full_path(self, hdfs_path):
        """Convert HDFS path ke local path"""
        # Remove leading slash
        clean_path = hdfs_path.lstrip('/')
        return self.base_path / clean_path
    
    def mkdir(self, path):
        """Membuat direktori"""
        full_path = self._get_full_path(path)
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {path}")
        return True
    
    def ls(self, path="/"):
        """List isi direktori"""
        full_path = self._get_full_path(path)
        
        if not full_path.exists():
            print(f"✗ Path not found: {path}")
            return []
        
        print(f"\n=== Listing: {path} ===")
        items = []
        
        for item in full_path.iterdir():
            is_dir = item.is_dir()
            size = item.stat().st_size if item.is_file() else 0
            modified = datetime.fromtimestamp(item.stat().st_mtime)
            
            item_type = "DIR " if is_dir else "FILE"
            print(f"{item_type} {size:>10} bytes  {modified.strftime('%Y-%m-%d %H:%M')}  {item.name}")
            
            items.append({
                'name': item.name,
                'type': 'directory' if is_dir else 'file',
                'size': size,
                'modified': modified
            })
        
        return items
    
    def put(self, local_path, hdfs_path):
        """Upload file ke 'HDFS'"""
        if not os.path.exists(local_path):
            print(f"✗ Local file not found: {local_path}")
            return False
        
        full_path = self._get_full_path(hdfs_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(local_path, full_path)
        size = os.path.getsize(local_path)
        print(f"✓ Uploaded: {local_path} -> {hdfs_path} ({size} bytes)")
        return True
    
    def get(self, hdfs_path, local_path):
        """Download file dari 'HDFS'"""
        full_path = self._get_full_path(hdfs_path)
        
        if not full_path.exists():
            print(f"✗ HDFS file not found: {hdfs_path}")
            return False
        
        shutil.copy2(full_path, local_path)
        size = os.path.getsize(local_path)
        print(f"✓ Downloaded: {hdfs_path} -> {local_path} ({size} bytes)")
        return True
    
    def cat(self, hdfs_path):
        """Menampilkan isi file"""
        full_path = self._get_full_path(hdfs_path)
        
        if not full_path.exists():
            print(f"✗ File not found: {hdfs_path}")
            return None
        
        print(f"\n=== Content of {hdfs_path} ===")
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        return content
    
    def rm(self, hdfs_path, recursive=False):
        """Hapus file atau direktori"""
        full_path = self._get_full_path(hdfs_path)
        
        if not full_path.exists():
            print(f"✗ Path not found: {hdfs_path}")
            return False
        
        if full_path.is_dir():
            if recursive:
                shutil.rmtree(full_path)
                print(f"✓ Removed directory (recursive): {hdfs_path}")
            else:
                print(f"✗ {hdfs_path} is a directory. Use recursive=True")
                return False
        else:
            full_path.unlink()
            print(f"✓ Removed file: {hdfs_path}")
        
        return True
    
    def du(self, path="/"):
        """Disk usage"""
        full_path = self._get_full_path(path)
        
        if not full_path.exists():
            print(f"✗ Path not found: {path}")
            return 0
        
        total_size = 0
        
        if full_path.is_file():
            total_size = full_path.stat().st_size
        else:
            for item in full_path.rglob('*'):
                if item.is_file():
                    total_size += item.stat().st_size
        
        # Format size
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024**2:
            size_str = f"{total_size/1024:.2f} KB"
        elif total_size < 1024**3:
            size_str = f"{total_size/(1024**2):.2f} MB"
        else:
            size_str = f"{total_size/(1024**3):.2f} GB"
        
        print(f"\n=== Disk Usage: {path} ===")
        print(f"Total: {size_str} ({total_size} bytes)")
        
        return total_size
    
    def cp(self, source, destination):
        """Copy file dalam HDFS"""
        src_path = self._get_full_path(source)
        dst_path = self._get_full_path(destination)
        
        if not src_path.exists():
            print(f"✗ Source not found: {source}")
            return False
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f"✓ Copied: {source} -> {destination}")
        return True
    
    def mv(self, source, destination):
        """Move file dalam HDFS"""
        src_path = self._get_full_path(source)
        dst_path = self._get_full_path(destination)
        
        if not src_path.exists():
            print(f"✗ Source not found: {source}")
            return False
        
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src_path, dst_path)
        print(f"✓ Moved: {source} -> {destination}")
        return True


def demo_without_hadoop():
    """Demo penggunaan tanpa Hadoop/Java"""
    print("=" * 70)
    print("DEMO: OPERASI FILE TERDISTRIBUSI TANPA HADOOP/JAVA")
    print("=" * 70)
    print()
    
    # Initialize Mock HDFS
    hdfs = MockHDFS("./mock_hdfs_storage")
    
    # Buat struktur direktori
    print("\n1. Membuat direktori...")
    hdfs.mkdir("/user/hadoop/input")
    hdfs.mkdir("/user/hadoop/output")
    
    # Upload file
    print("\n2. Upload file...")
    # Buat sample file dulu
    with open("test_data.txt", "w") as f:
        f.write("Hello World\nBig Data Processing\nPython Hadoop Alternative\n")
    
    hdfs.put("test_data.txt", "/user/hadoop/input/data.txt")
    
    # List direktori
    print("\n3. List direktori...")
    hdfs.ls("/user/hadoop/input")
    
    # Baca file
    print("\n4. Baca file...")
    hdfs.cat("/user/hadoop/input/data.txt")
    
    # Copy file
    print("\n5. Copy file...")
    hdfs.cp("/user/hadoop/input/data.txt", "/user/hadoop/output/result.txt")
    
    # Disk usage
    print("\n6. Disk usage...")
    hdfs.du("/user/hadoop")
    
    # Download file
    print("\n7. Download file...")
    hdfs.get("/user/hadoop/output/result.txt", "downloaded_result.txt")
    
    # List semua
    print("\n8. List root...")
    hdfs.ls("/")
    
    print("\n" + "=" * 70)
    print("✅ SELESAI! Semua operasi berhasil TANPA Java/Hadoop!")
    print("=" * 70)


if __name__ == "__main__":
    demo_without_hadoop()
