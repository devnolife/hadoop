"""
Quick Start Examples for Hadoop Python Toolkit
"""

from src.hdfs_operations import HDFSOperations
from src.database_to_hdfs import DatabaseToHDFS

def example_hdfs_basic():
    """Basic HDFS operations example"""
    print("=" * 60)
    print("Example 1: Basic HDFS Operations")
    print("=" * 60)
    
    hdfs = HDFSOperations()
    
    # Create directory
    hdfs.create_directory("/user/data/input")
    
    # Upload file
    hdfs.upload_file("data/samples/sample_data.txt", "/user/data/input/")
    
    # List files
    hdfs.list_directory("/user/data/input")
    
    # Download file
    hdfs.download_file("/user/data/input/sample_data.txt", "output.txt")
    
    print("\n✓ Basic operations completed!")


def example_database_export():
    """Database to HDFS example"""
    print("\n" + "=" * 60)
    print("Example 2: Export Database to HDFS")
    print("=" * 60)
    
    db_to_hdfs = DatabaseToHDFS()
    
    # MySQL configuration example
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'mydb'
    }
    
    print("\nTo export from MySQL to HDFS:")
    print("db_to_hdfs.mysql_to_hdfs(")
    print("    db_config=mysql_config,")
    print("    table='customers',")
    print("    hdfs_path='/user/data/customers.csv'")
    print(")")
    
    print("\n✓ Example configuration shown!")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           HADOOP PYTHON TOOLKIT - QUICK START                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Run examples
    # example_hdfs_basic()  # Uncomment to run with actual Hadoop
    example_database_export()
    
    print("\n" + "=" * 60)
    print("For more examples, check the examples/ directory")
    print("=" * 60)
