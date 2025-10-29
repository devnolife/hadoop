<div align="center">

# 🐘 Hadoop Python Toolkit

### Modern Python Interface for Apache Hadoop & Big Data Processing

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.x-orange.svg)](https://hadoop.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-devnolife-red.svg)](https://github.com/devnolife)

*Simplify Hadoop operations with Python. No complex Java setup required!*

[Features](#-features) •
[Quick Start](#-quick-start) •
[Installation](#-installation) •
[Documentation](#-documentation) •
[Examples](#-examples)

</div>

---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🔥 Core Features
- **Easy HDFS Operations** - Upload, download, manage files
- **Database Integration** - MySQL/PostgreSQL to HDFS
- **Docker Support** - One-command Hadoop cluster
- **Mock HDFS** - Development without Hadoop
- **Cross-Platform** - Windows, Linux, macOS

</td>
<td width="50%">

### 🚀 Technologies
- **Python 3.8+** - Modern Python
- **Apache Hadoop 3.x** - Big Data framework
- **Docker** - Containerization
- **Dask/Pandas** - Data processing
- **Well Documented** - Complete guides

</td>
</tr>
</table>

---

## ⚡ Quick Start

### Option 1: Docker (Recommended) 🐳

```bash
# Start Hadoop cluster (one command!)
docker-compose up -d

# Access web interfaces
# NameNode: http://localhost:9870
# ResourceManager: http://localhost:8088
```

### Option 2: Mock HDFS (No Hadoop Needed!)

```python
from examples.mock_hdfs_demo import MockHDFS

# Initialize mock HDFS
hdfs = MockHDFS("./storage")

# Use like real HDFS!
hdfs.mkdir("/data")
hdfs.put("file.txt", "/data/file.txt")
hdfs.ls("/data")
```

### Option 3: Native Hadoop

```python
from src.hdfs_operations import HDFSOperations

hdfs = HDFSOperations()
hdfs.create_directory("/user/data")
hdfs.upload_file("data.txt", "/user/data/")
hdfs.list_directory("/user/data")
```

---

## 🎯 Usage Examples

### 1️⃣ Basic HDFS Operations

```python
from src.hdfs_operations import HDFSOperations

hdfs = HDFSOperations()

# Create directories
hdfs.create_directory("/user/hadoop/input")
hdfs.create_directory("/user/hadoop/output")

# Upload files
hdfs.upload_file('data.csv', '/user/hadoop/input/')

# List files
hdfs.list_directory('/user/hadoop')

# Download results
hdfs.download_file('/user/hadoop/output/result.csv', 'result.csv')

# View file content
hdfs.cat_file('/user/hadoop/input/data.csv')

# Check disk usage
hdfs.disk_usage('/user/hadoop')
```

### 2️⃣ Database to HDFS Migration

```python
from src.database_to_hdfs import DatabaseToHDFS

db_to_hdfs = DatabaseToHDFS()

# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'mydb'
}

# Export table to HDFS
db_to_hdfs.mysql_to_hdfs(
    db_config=mysql_config,
    table='customers',
    hdfs_path='/user/data/customers.csv'
)

# PostgreSQL support
postgres_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'password',
    'database': 'mydb'
}

db_to_hdfs.postgres_to_csv(
    **postgres_config,
    table='orders',
    output_file='orders.csv'
)
```

### 3️⃣ Big Data Processing (No Hadoop!)

```python
import dask.dataframe as dd

# Read large CSV file
df = dd.read_csv('huge_file.csv')

# Process in parallel
result = df[df['value'] > 1000].groupby('category').sum()

# Compute results
result.compute()

# Save to file
result.to_csv('output.csv', index=False)
```

### 4️⃣ Hadoop Commands Reference

```python
from src.hadoop_commands import HadoopCommandGuide

guide = HadoopCommandGuide()

# View all commands
guide.print_commands()

# Search specific command
guide.search_command('upload')

# View specific category
guide.print_commands('file_operations')
```

## � Installation

### Prerequisites

Choose your setup method:

<details>
<summary><b>🐳 Docker Setup (Easiest!)</b></summary>

**Requirements:**
- Docker Desktop installed
- 4GB+ RAM available

**Installation:**
```bash
# Clone repository
git clone https://github.com/devnolife/hadoop-python-toolkit.git
cd hadoop-python-toolkit

# Start Hadoop cluster
docker-compose up -d

# Verify
docker-compose ps
```

**Access Web UIs:**
- NameNode: http://localhost:9870
- ResourceManager: http://localhost:8088
- History Server: http://localhost:8188

</details>

<details>
<summary><b>💻 Native Hadoop Setup</b></summary>

**Windows:**
```powershell
# 1. Install Java JDK 8 or 11
java -version

# 2. Download Hadoop
# Get from: https://hadoop.apache.org/releases.html
# Extract to: C:\hadoop

# 3. Set environment variables (as Administrator)
setx HADOOP_HOME "C:\hadoop" /M
setx JAVA_HOME "C:\Program Files\Java\jdk-11" /M
setx PATH "%PATH%;%HADOOP_HOME%\bin" /M

# 4. Download winutils
# From: https://github.com/kontext-tech/winutils
# Copy to: C:\hadoop\bin\
```

**Linux/Mac:**
```bash
# Install Java
sudo apt install openjdk-11-jdk  # Ubuntu/Debian
brew install openjdk@11           # macOS

# Download Hadoop
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop

# Set environment
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin' >> ~/.bashrc
source ~/.bashrc
```

</details>

<details>
<summary><b>🐍 Python-Only Setup (No Hadoop!)</b></summary>

**Just Python needed:**
```bash
# Install Python 3.8+
python --version

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Use Mock HDFS
python examples/mock_hdfs_demo.py
```

</details>

### Python Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Optional: Database connectors
pip install mysql-connector-python  # MySQL
pip install psycopg2-binary         # PostgreSQL

# Optional: Big data libraries
pip install dask[complete]          # Parallel processing
pip install polars                  # Fast dataframes
```

## �️ Project Structure

```
hadoop-python-toolkit/
│
├── 📁 src/                          # Core modules
│   ├── __init__.py                  # Package initialization
│   ├── hdfs_operations.py           # HDFS operations
│   ├── database_to_hdfs.py          # Database export
│   ├── hadoop_setup.py              # Setup utilities
│   └── hadoop_commands.py           # Command reference
│
├── 📁 examples/                     # Usage examples
│   ├── quick_start.py               # Quick start guide
│   ├── mock_hdfs_demo.py            # Mock HDFS demo
│   └── python_alternatives_demo.py  # Alternative tools
│
├── 📁 docs/                         # Documentation
│   ├── installation.md              # Installation guide
│   ├── getting-started.md           # Getting started
│   └── docker-commands.md           # Docker commands
│
├── 📁 data/                         # Data directory
│   └── samples/                     # Sample data files
│
├── docker-compose.yml               # Docker Hadoop cluster
├── hadoop.env                       # Hadoop environment config
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
└── README.md                        # This file
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/installation.md) | Detailed setup instructions |
| [Getting Started](docs/getting-started.md) | Beginner-friendly tutorial |
| [Docker Commands](docs/docker-commands.md) | Docker reference guide |
| [Examples](examples/) | Code examples and demos |

---

## 🎓 What You Can Do

✅ **Hadoop Setup** - Single node & cluster configuration  
✅ **HDFS Operations** - File management and operations  
✅ **Data Transfer** - Upload/download files to/from HDFS  
✅ **Database Migration** - Export MySQL/PostgreSQL to HDFS  
✅ **Command Reference** - Complete Hadoop command guide  
✅ **Docker Deployment** - Containerized Hadoop cluster  
✅ **Mock Development** - Test without Hadoop installation  
✅ **Big Data Processing** - Alternative Python tools

## � Development Workflow

### Using Docker

```bash
# Start cluster
docker-compose up -d

# Check status
docker-compose ps

# Execute HDFS commands
docker exec -it namenode hdfs dfs -ls /

# Copy files to container
docker cp data.txt namenode:/tmp/

# View logs
docker logs namenode

# Stop cluster
docker-compose down
```

### Using Native Hadoop

```bash
# Format NameNode (first time only)
hdfs namenode -format

# Start services
start-all.sh     # Linux/Mac
start-dfs.cmd    # Windows
start-yarn.cmd   # Windows

# Test HDFS
hdfs dfs -mkdir -p /user/hadoop/test
hdfs dfs -ls /

# Stop services
stop-all.sh      # Linux/Mac
```

### Using Mock HDFS

```bash
# Run mock HDFS demo
python examples/mock_hdfs_demo.py

# Run quick start example
python examples/quick_start.py

# View command reference
python src/hadoop_commands.py
```

## � Best Practices

<table>
<tr>
<td width="50%">

### ✅ Do's
- ✓ Use Docker for development
- ✓ Use absolute paths in HDFS
- ✓ Monitor disk usage regularly
- ✓ Backup data before formatting
- ✓ Use virtual environments
- ✓ Handle errors gracefully

</td>
<td width="50%">

### ❌ Don'ts
- ✗ Don't format NameNode in production
- ✗ Don't use root user
- ✗ Don't ignore disk space warnings
- ✗ Don't skip backups
- ✗ Don't hardcode credentials
- ✗ Don't forget to stop services

</td>
</tr>
</table>

---

## 🎨 Comparison: Hadoop vs Alternatives

| Feature | Hadoop | Dask | Polars | Pandas |
|---------|--------|------|--------|--------|
| **Setup** | Complex | Easy | Easy | Easy |
| **Java Required** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Distributed** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Speed** | Medium | Fast | Very Fast | Medium |
| **Learning Curve** | Steep | Medium | Low | Low |
| **Best For** | Production | Big Data | Fast Processing | Analysis |

---

## � Performance Tips

```python
# 1. Use chunking for large files
import pandas as pd
for chunk in pd.read_csv('large.csv', chunksize=10000):
    process(chunk)

# 2. Use Dask for parallel processing
import dask.dataframe as dd
df = dd.read_csv('large.csv')
result = df.compute()

# 3. Monitor HDFS disk usage
hdfs.disk_usage('/user/hadoop')

# 4. Use compression
hdfs.upload_file('data.csv.gz', '/user/data/')
```

## 🐛 Troubleshooting

<details>
<summary><b>Command not found</b></summary>

**Problem:** `hadoop: command not found` or `hdfs: command not found`

**Solution:**
```bash
# Check HADOOP_HOME
echo $HADOOP_HOME  # Linux/Mac
echo %HADOOP_HOME%  # Windows

# Set HADOOP_HOME
export HADOOP_HOME=/usr/local/hadoop  # Linux/Mac
setx HADOOP_HOME "C:\hadoop" /M       # Windows

# Add to PATH
export PATH=$PATH:$HADOOP_HOME/bin    # Linux/Mac
```
</details>

<details>
<summary><b>Connection refused</b></summary>

**Problem:** `Connection refused` when accessing web UI

**Solution:**
```bash
# Check if services are running
jps  # Should show NameNode, DataNode, etc.

# Start services
start-all.sh  # Linux/Mac
start-dfs.cmd && start-yarn.cmd  # Windows

# Check ports
netstat -an | grep 9870  # NameNode
netstat -an | grep 8088  # ResourceManager
```
</details>

<details>
<summary><b>Permission denied</b></summary>

**Problem:** `Permission denied` when accessing HDFS

**Solution:**
```bash
# Check permissions
hdfs dfs -ls -R /

# Change permissions
hdfs dfs -chmod -R 777 /user/hadoop

# Change owner
hdfs dfs -chown -R hadoop:hadoop /user/hadoop
```
</details>

<details>
<summary><b>Docker issues</b></summary>

**Problem:** Docker container won't start

**Solution:**
```bash
# Check Docker status
docker ps

# View logs
docker logs namenode

# Restart containers
docker-compose restart

# Clean start
docker-compose down -v
docker-compose up -d
```
</details>

<details>
<summary><b>Port already in use</b></summary>

**Problem:** `Address already in use`

**Solution:**
```bash
# Find process using port
netstat -ano | findstr :9870  # Windows
lsof -i :9870                 # Linux/Mac

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac

# Or use different ports in hadoop config
```
</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 devnolife

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- **Apache Hadoop** - The foundation of big data processing
- **Python Community** - For amazing libraries and tools
- **Docker** - Making deployment simple
- **Contributors** - Everyone who helps improve this project

---

## 📧 Contact & Support

<div align="center">

**Created by [devnolife](https://github.com/devnolife)**

[![GitHub](https://img.shields.io/badge/GitHub-devnolife-black?logo=github)](https://github.com/devnolife)
[![Email](https://img.shields.io/badge/Email-Contact-blue?logo=gmail)](mailto:your.email@example.com)

For questions, issues, or suggestions:
- 🐛 [Open an Issue](https://github.com/devnolife/hadoop-python-toolkit/issues)
- 💬 [Start a Discussion](https://github.com/devnolife/hadoop-python-toolkit/discussions)
- ⭐ Star this repo if you find it helpful!

</div>

---

## 🗺️ Roadmap

- [x] Basic HDFS operations
- [x] Database integration
- [x] Docker support
- [x] Mock HDFS for development
- [x] Comprehensive documentation
- [ ] Web UI for operations
- [ ] REST API interface
- [ ] Monitoring dashboard
- [ ] Automated testing
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Spark integration

---

<div align="center">

### ⭐ If you find this helpful, please star the repo!

**Made with ❤️ by [devnolife](https://github.com/devnolife)**

</div>
