# Installation Guide

## Prerequisites

### Option 1: Using Docker (Recommended) 🐳

Docker provides the easiest way to run Hadoop without complex setup.

#### Requirements
- Docker Desktop installed
- 4GB+ RAM available

#### Quick Start
```bash
# Clone or download this project
cd hadoop-python-toolkit

# Start Hadoop cluster
docker-compose up -d

# Verify
docker-compose ps

# Access UIs
# NameNode: http://localhost:9870
# ResourceManager: http://localhost:8088
```

---

### Option 2: Native Hadoop Installation

#### Windows
1. **Install Java JDK 8 or 11**
   ```powershell
   # Download from: https://www.oracle.com/java/technologies/downloads/
   # Verify installation
   java -version
   ```

2. **Download Hadoop**
   - Get Hadoop from: https://hadoop.apache.org/releases.html
   - Download winutils: https://github.com/kontext-tech/winutils
   - Extract to `C:\hadoop`

3. **Set Environment Variables**
   ```powershell
   # As Administrator
   setx HADOOP_HOME "C:\hadoop" /M
   setx JAVA_HOME "C:\Program Files\Java\jdk-11" /M
   setx PATH "%PATH%;%HADOOP_HOME%\bin;%HADOOP_HOME%\sbin" /M
   ```

4. **Configure Hadoop**
   - Edit files in `C:\hadoop\etc\hadoop\`
   - See `docs/configuration.md` for details

#### Linux/Mac
```bash
# Install Java
sudo apt install openjdk-11-jdk  # Ubuntu/Debian
brew install openjdk@11           # macOS

# Download and extract Hadoop
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop

# Set environment variables
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
source ~/.bashrc
```

---

## Python Setup

### Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Optional: Database Connectors
```bash
# For MySQL
pip install mysql-connector-python

# For PostgreSQL
pip install psycopg2-binary

# For Big Data alternatives (No Hadoop needed)
pip install dask[complete]
pip install polars
```

---

## Verification

### Test Hadoop Installation
```bash
# Format NameNode (first time only)
hdfs namenode -format

# Start services
start-dfs.sh   # Linux/Mac
start-dfs.cmd  # Windows

# Verify
hdfs dfs -ls /
```

### Test Python Toolkit
```python
from src.hdfs_operations import HDFSOperations

hdfs = HDFSOperations()
hdfs.create_directory("/test")
hdfs.list_directory("/")
```

---

## Troubleshooting

### Common Issues

**Port already in use**
- Check if services are running: `jps`
- Stop services: `stop-all.sh`

**Permission denied**
- Windows: Run as Administrator
- Linux: Check file permissions

**Connection refused**
- Verify Hadoop is running
- Check firewall settings
- Ensure correct ports (9870, 8088)

**Java not found**
- Verify JAVA_HOME is set correctly
- Add Java to PATH

---

## Next Steps

1. Read [Getting Started Guide](getting-started.md)
2. Try [Examples](../examples/)
3. Check [API Documentation](api-reference.md)
