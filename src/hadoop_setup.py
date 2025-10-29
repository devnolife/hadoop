"""
Script untuk Setup dan Konfigurasi Hadoop
Teknologi Big Data
"""

import os
import subprocess
import platform

class HadoopSetup:
    def __init__(self):
        self.os_type = platform.system()
        
    def check_java(self):
        """Memeriksa instalasi Java"""
        print("Memeriksa instalasi Java...")
        try:
            result = subprocess.run(['java', '-version'], 
                                  capture_output=True, 
                                  text=True)
            print("✓ Java sudah terinstal")
            print(result.stderr)
            return True
        except FileNotFoundError:
            print("✗ Java belum terinstal")
            print("Silakan install Java terlebih dahulu")
            return False
    
    def setup_single_node(self):
        """Setup Hadoop Single Node"""
        print("\n=== Setup Hadoop Single Node ===")
        print("1. Download Hadoop dari Apache Website")
        print("2. Extract ke direktori pilihan")
        print("3. Set environment variables:")
        print("   - HADOOP_HOME")
        print("   - JAVA_HOME")
        print("4. Konfigurasi core-site.xml")
        print("5. Konfigurasi hdfs-site.xml")
        print("6. Konfigurasi mapred-site.xml")
        print("7. Konfigurasi yarn-site.xml")
        
    def setup_cluster(self):
        """Setup Hadoop Cluster"""
        print("\n=== Setup Hadoop Cluster ===")
        print("1. Siapkan multiple machines/VMs")
        print("2. Install Hadoop di semua nodes")
        print("3. Konfigurasi Master Node:")
        print("   - NameNode")
        print("   - ResourceManager")
        print("4. Konfigurasi Worker Nodes:")
        print("   - DataNode")
        print("   - NodeManager")
        print("5. Setup SSH passwordless authentication")
        print("6. Konfigurasi workers file")
        
    def format_namenode(self):
        """Format HDFS NameNode"""
        print("\n=== Format NameNode ===")
        print("Command: hdfs namenode -format")
        
        if self.os_type == "Windows":
            print("\nUntuk Windows:")
            print("hadoop namenode -format")
        else:
            print("\nUntuk Linux/Mac:")
            print("hdfs namenode -format")

if __name__ == "__main__":
    setup = HadoopSetup()
    
    print("=" * 50)
    print("HADOOP SETUP - SINGLE NODE & CLUSTER")
    print("=" * 50)
    
    # Check Java
    setup.check_java()
    
    # Setup guides
    setup.setup_single_node()
    setup.setup_cluster()
    setup.format_namenode()
