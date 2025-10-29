# Getting Started Guide

## Introduction

This toolkit provides Python interfaces for Hadoop operations, making it easy to work with HDFS and process big data.

## Basic Concepts

### HDFS (Hadoop Distributed File System)
- Distributed storage system
- Fault-tolerant and scalable
- Designed for large files

### MapReduce
- Programming model for processing large datasets
- Parallel and distributed computing

---

## Quick Start

### 1. Simple HDFS Operations

```python
from src.hdfs_operations import HDFSOperations

# Initialize
hdfs = HDFSOperations()

# Create directory
hdfs.create_directory("/user/mydata")

# Upload file
hdfs.upload_file("local_file.txt", "/user/mydata/")

# List contents
hdfs.list_directory("/user/mydata")

# Download file
hdfs.download_file("/user/mydata/local_file.txt", "downloaded.txt")

# View file content
hdfs.cat_file("/user/mydata/local_file.txt")
```

### 2. Database to HDFS

```python
from src.database_to_hdfs import DatabaseToHDFS

# Initialize
db_to_hdfs = DatabaseToHDFS()

# MySQL configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'mydb'
}

# Export table to HDFS
db_to_hdfs.mysql_to_hdfs(
    db_config=mysql_config,
    table='users',
    hdfs_path='/user/data/users.csv'
)
```

### 3. Using Mock HDFS (No Hadoop Needed)

```python
from examples.mock_hdfs_demo import MockHDFS

# Initialize mock HDFS
hdfs = MockHDFS("./my_storage")

# Use same commands as real HDFS
hdfs.mkdir("/data/input")
hdfs.put("file.txt", "/data/input/file.txt")
hdfs.ls("/data/input")
hdfs.get("/data/input/file.txt", "output.txt")
```

---

## Common Operations

### File Management

```python
# Create nested directories
hdfs.create_directory("/user/project/input")

# Upload multiple files
for file in ["data1.txt", "data2.txt", "data3.txt"]:
    hdfs.upload_file(file, "/user/project/input/")

# Copy within HDFS
hdfs.run_command("hdfs dfs -cp /source/file.txt /destination/")

# Move files
hdfs.run_command("hdfs dfs -mv /old/path /new/path")

# Remove files
hdfs.remove_file("/user/project/temp.txt")
```

### Monitoring

```python
# Check disk usage
hdfs.disk_usage("/user/project")

# Get file info
hdfs.get_file_info("/user/project/data.txt")

# List with details
hdfs.list_directory("/user/project")
```

---

## Working with Data

### Text Files

```python
# Upload text file
hdfs.upload_file("data.txt", "/input/data.txt")

# Read content
content = hdfs.cat_file("/input/data.txt")

# Process line by line
lines = content.split('\n')
for line in lines:
    print(line)
```

### CSV Files

```python
import pandas as pd

# Create CSV locally
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})
df.to_csv('data.csv', index=False)

# Upload to HDFS
hdfs.upload_file('data.csv', '/data/users.csv')

# Download and process
hdfs.download_file('/data/users.csv', 'downloaded.csv')
df = pd.read_csv('downloaded.csv')
print(df.head())
```

---

## Advanced Usage

### Batch Operations

```python
def batch_upload(local_dir, hdfs_dir):
    """Upload all files from local directory"""
    import os
    
    hdfs = HDFSOperations()
    hdfs.create_directory(hdfs_dir)
    
    for file in os.listdir(local_dir):
        local_path = os.path.join(local_dir, file)
        if os.path.isfile(local_path):
            hdfs.upload_file(local_path, hdfs_dir)
            print(f"Uploaded: {file}")

# Usage
batch_upload("./local_data", "/hdfs/batch_data")
```

### Error Handling

```python
try:
    hdfs.upload_file("file.txt", "/user/data/")
except FileNotFoundError:
    print("Local file not found")
except Exception as e:
    print(f"Error: {e}")
```

---

## Alternative: Python-Only Solutions

If you don't want to install Hadoop:

### Using Dask

```python
import dask.dataframe as dd

# Read large CSV
df = dd.read_csv('large_file.csv')

# Process
result = df[df['value'] > 100].compute()

# Save
result.to_csv('output.csv', index=False)
```

### Using Pandas Chunking

```python
import pandas as pd

# Process large file in chunks
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = chunk[chunk['value'] > 100]
    # Save or aggregate
    processed.to_csv('output.csv', mode='a', index=False)
```

---

## Best Practices

1. **Always check paths**
   ```python
   hdfs.list_directory("/")  # Check before operations
   ```

2. **Use absolute paths**
   ```python
   hdfs.upload_file("/full/path/to/file.txt", "/user/data/")
   ```

3. **Clean up temporary files**
   ```python
   hdfs.remove_file("/temp/file.txt")
   ```

4. **Monitor disk usage**
   ```python
   hdfs.disk_usage("/user/project")
   ```

5. **Handle errors gracefully**
   ```python
   try:
       hdfs.upload_file(file, path)
   except Exception as e:
       logging.error(f"Failed to upload: {e}")
   ```

---

## Next Steps

- Explore [Examples](../examples/)
- Read [API Reference](api-reference.md)
- Check [Configuration Guide](configuration.md)
- Try [Docker Setup](docker-setup.md)
