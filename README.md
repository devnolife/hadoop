# Hadoop Big Data Processing - Complete Guide

Project pembelajaran Apache Hadoop untuk big data processing dengan setup single node dan multi-node cluster, dilengkapi script interaktif yang keren!

## 🎯 Quick Start

### Super Easy Way - Run Master Script!

```bash
./hadoop-master.sh
```

Script all-in-one dengan menu interaktif untuk:
- ✓ Install & configure Hadoop
- ✓ Setup database integration
- ✓ Start/stop services
- ✓ Web dashboard guide
- ✓ Run examples

**Cukup 1 command!** 🚀

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [HDFS Operations](#hdfs-operations)
6. [MapReduce Examples](#mapreduce-examples)
7. [Database Integration](#database-integration)
8. [Web Interfaces](#web-interfaces)
9. [Cluster Setup](#cluster-setup)
10. [Troubleshooting](#troubleshooting)
11. [Commands Cheat Sheet](#commands-cheat-sheet)

---

## System Requirements

### Hardware (Minimum)
- CPU: 2 cores
- RAM: 4GB (8GB recommended)
- Storage: 20GB free space

### Software (Already Included)
- ✅ Java 11 (OpenJDK 11.0.2) - sudah terinstall di `jdk-11.0.2/`
- ✅ Hadoop 3.3.6 - akan didownload/extracted
- ✅ Linux (Ubuntu/Debian/WSL2)

---

## Project Structure

```
hdoop/
├── hadoop-master.sh           # 🎯 MAIN SCRIPT - RUN THIS!
│
├── jdk-11.0.2/                # Java installation
│
├── hadoop/
│   ├── hadoop-3.3.6.tar.gz   # Hadoop archive (downloading)
│   ├── hadoop-3.3.6/         # Extracted Hadoop
│   └── config/               # Configuration files
│       ├── core-site.xml
│       ├── hdfs-site.xml
│       ├── mapred-site.xml
│       ├── yarn-site.xml
│       └── workers
│
├── data/
│   ├── input/                # Sample input files
│   └── output/               # Results
│
├── scripts/
│   ├── env-setup.sh          # Environment variables
│   ├── start-hadoop.sh       # Start services
│   ├── stop-hadoop.sh        # Stop services
│   └── examples/             # Example scripts
│
└── docs/                     # Additional documentation
```

---

## Installation

### Method 1: Interactive Master Script (RECOMMENDED)

```bash
./hadoop-master.sh
```

Pilih menu: **1) Install & Configure Hadoop**

Script akan otomatis:
1. ✓ Check download completion
2. ✓ Extract Hadoop (696MB)
3. ✓ Copy configurations
4. ✓ Setup environment
5. ✓ Configure SSH
6. ✓ Create directories
7. ✓ Format NameNode
8. ✓ Start services

### Method 2: Manual Steps

```bash
# 1. Extract Hadoop
cd hadoop
tar -xzf hadoop-3.3.6.tar.gz
cd ..

# 2. Copy configurations
cp hadoop/config/*.xml hadoop/hadoop-3.3.6/etc/hadoop/
echo "export JAVA_HOME=/home/devnolife/hdoop/jdk-11.0.2" >> hadoop/hadoop-3.3.6/etc/hadoop/hadoop-env.sh

# 3. Setup environment
source scripts/env-setup.sh

# 4. Setup SSH
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# 5. Create directories
mkdir -p hadoop/data/namenode hadoop/data/datanode hadoop/tmp

# 6. Format NameNode
hdfs namenode -format -force

# 7. Start services
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh
```

---

## Configuration

### Key Configuration Files

#### 1. core-site.xml
```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
</property>
```

#### 2. hdfs-site.xml
```xml
<property>
    <name>dfs.replication</name>
    <value>1</value>  <!-- Single node -->
</property>
<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/devnolife/hdoop/hadoop/data/namenode</value>
</property>
```

#### 3. mapred-site.xml
```xml
<property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
</property>
```

#### 4. yarn-site.xml
```xml
<property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
</property>
```

### Important Ports

| Service | Port | URL |
|---------|------|-----|
| NameNode Web UI | 9870 | http://localhost:9870 |
| ResourceManager UI | 8088 | http://localhost:8088 |
| DataNode UI | 9864 | http://localhost:9864 |
| NameNode RPC | 9000 | - |

---

## HDFS Operations

### Using Master Script

```bash
./hadoop-master.sh
# Select: 7) Run HDFS & MapReduce Examples
# Then: 1) HDFS Basic Commands
```

### Manual Commands

```bash
# Load environment
source scripts/env-setup.sh

# Create directories
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -mkdir -p /user/hadoop/output

# Upload file
hdfs dfs -put data/input/sample-data.txt /user/hadoop/input/

# List files
hdfs dfs -ls /user/hadoop/input/

# View file
hdfs dfs -cat /user/hadoop/input/sample-data.txt

# Download file
hdfs dfs -get /user/hadoop/input/sample-data.txt ./

# Copy within HDFS
hdfs dfs -cp /user/hadoop/input/file1.txt /user/hadoop/input/file2.txt

# Delete file
hdfs dfs -rm /user/hadoop/input/file.txt

# Delete directory
hdfs dfs -rm -r /user/hadoop/temp/

# Check storage
hdfs dfs -du -h /user/hadoop/

# Cluster status
hdfs dfsadmin -report
```

---

## MapReduce Examples

### WordCount Example

#### Using Master Script
```bash
./hadoop-master.sh
# Select: 7) Run HDFS & MapReduce Examples
# Then: 2) WordCount MapReduce
```

#### Manual Execution
```bash
source scripts/env-setup.sh

# Prepare input
hdfs dfs -mkdir -p /user/hadoop/wordcount/input
hdfs dfs -put data/input/word-count-input.txt /user/hadoop/wordcount/input/

# Run MapReduce
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
  wordcount /user/hadoop/wordcount/input /user/hadoop/wordcount/output

# View results
hdfs dfs -cat /user/hadoop/wordcount/output/part-r-00000
```

### Available MapReduce Examples

```bash
# List all examples
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar

# Examples include:
# - wordcount: Count words in files
# - grep: Search patterns
# - pi: Calculate pi
# - terasort: Sort large datasets
# - and more...
```

---

## Database Integration

### Interactive Setup

```bash
./hadoop-master.sh
# Select: 2) Setup Database Integration
```

Wizard akan meminta:
1. Database type (MySQL/PostgreSQL/Oracle/SQL Server)
2. Host (default: localhost)
3. Port (default by DB type)
4. Database name
5. Username
6. Password (secure input)
7. Table name

### Supported Databases

| Database | Default Port | JDBC Driver |
|----------|--------------|-------------|
| MySQL | 3306 | com.mysql.jdbc.Driver |
| PostgreSQL | 5432 | org.postgresql.Driver |
| Oracle | 1521 | oracle.jdbc.driver.OracleDriver |
| SQL Server | 1433 | com.microsoft.sqlserver.jdbc.SQLServerDriver |

### Sqoop Commands (Generated Automatically)

```bash
# Import single table
sqoop import \
  --connect "jdbc:mysql://localhost:3306/mydb" \
  --username root \
  --password password \
  --table users \
  --target-dir "/user/hadoop/sqoop/users" \
  --m 1

# Import with query
sqoop import \
  --connect "jdbc:mysql://localhost:3306/mydb" \
  --username root \
  --password password \
  --query "SELECT * FROM users WHERE age > 30 AND \$CONDITIONS" \
  --target-dir "/user/hadoop/sqoop/users_filtered" \
  --split-by id \
  --m 1

# Import incremental
sqoop import \
  --connect "jdbc:mysql://localhost:3306/mydb" \
  --username root \
  --password password \
  --table users \
  --incremental append \
  --check-column id \
  --last-value 0 \
  --m 1
```

**Note**: Sqoop harus diinstall terpisah. Script akan generate commands yang siap digunakan.

---

## Web Interfaces

### Access Web UIs

```bash
./hadoop-master.sh
# Select: 5) Web Dashboard Guide
```

### NameNode UI (Port 9870)

**URL**: http://localhost:9870

**Features**:
- Overview: Cluster capacity, live/dead nodes
- Datanodes: Individual node health
- Browse Filesystem: Navigate HDFS
- Logs: Debug and troubleshooting

**How It Works**:
1. Client requests file metadata
2. NameNode returns block locations
3. Client reads/writes directly to DataNodes
4. NameNode monitors via heartbeat

### ResourceManager UI (Port 8088)

**URL**: http://localhost:8088

**Features**:
- Cluster Metrics: CPU, memory, containers
- Applications: Running/finished jobs
- Nodes: NodeManager status
- Scheduler: Resource allocation

**How It Works**:
1. Client submits application
2. ResourceManager schedules
3. ApplicationMaster coordinates tasks
4. Tasks run in containers on NodeManagers
5. Progress tracked and resources released

### DataNode UI (Port 9864)

**URL**: http://localhost:9864

**Features**:
- Storage information
- Block statistics
- Logs

---

## Cluster Setup

### Multi-Node Setup Steps

1. **Prepare Nodes** (3+ machines)
   - Master: NameNode + ResourceManager
   - Workers: DataNode + NodeManager

2. **Configure Network**
   ```bash
   # Edit /etc/hosts on all nodes
   192.168.1.10  hadoop-master
   192.168.1.11  hadoop-worker1
   192.168.1.12  hadoop-worker2
   ```

3. **Setup SSH** (from master)
   ```bash
   ssh-keygen -t rsa -P ''
   ssh-copy-id hadoop-worker1
   ssh-copy-id hadoop-worker2
   ```

4. **Install Hadoop on All Nodes**
   - Copy installation to all nodes
   - Update configuration files

5. **Configure Workers**
   ```bash
   # Edit hadoop/hadoop-3.3.6/etc/hadoop/workers
   hadoop-worker1
   hadoop-worker2
   ```

6. **Update Configuration**
   ```xml
   <!-- core-site.xml -->
   <property>
       <name>fs.defaultFS</name>
       <value>hdfs://hadoop-master:9000</value>
   </property>

   <!-- yarn-site.xml -->
   <property>
       <name>yarn.resourcemanager.hostname</name>
       <value>hadoop-master</value>
   </property>
   ```

7. **Format & Start** (from master only)
   ```bash
   hdfs namenode -format
   start-dfs.sh
   start-yarn.sh
   ```

---

## Troubleshooting

### Services Won't Start

```bash
# Check logs
tail -f hadoop/hadoop-3.3.6/logs/*.log

# Check ports
netstat -tuln | grep -E '9000|9870|8088'

# Reformat NameNode (⚠️ deletes data)
hdfs namenode -format -force
```

### Permission Denied

```bash
# Reload environment
source scripts/env-setup.sh

# Check SSH
ssh localhost

# Fix SSH if needed
chmod 0600 ~/.ssh/authorized_keys
```

### Cannot Connect to NameNode

```bash
# Check if running
jps | grep NameNode

# Restart services
./hadoop-master.sh
# Select: 4) Stop Services
# Then: 3) Start Services
```

### Java Not Found

```bash
# Verify Java
echo $JAVA_HOME
java -version

# Reload environment
source scripts/env-setup.sh
```

### Out of Memory

```bash
# Edit yarn-site.xml
<property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>2048</value>  <!-- Reduce if needed -->
</property>
```

---

## Commands Cheat Sheet

### Service Management

```bash
# Using master script
./hadoop-master.sh
# Select: 3) Start or 4) Stop

# Manual
start-dfs.sh                # Start HDFS
start-yarn.sh               # Start YARN
stop-yarn.sh                # Stop YARN
stop-dfs.sh                 # Stop HDFS
jps                         # Check running processes
```

### HDFS Commands

```bash
hdfs dfs -ls <path>                     # List files
hdfs dfs -mkdir -p <path>               # Create directory
hdfs dfs -put <local> <hdfs>            # Upload
hdfs dfs -get <hdfs> <local>            # Download
hdfs dfs -cat <path>                    # View file
hdfs dfs -rm <path>                     # Delete file
hdfs dfs -rm -r <path>                  # Delete directory
hdfs dfs -cp <src> <dst>                # Copy
hdfs dfs -mv <src> <dst>                # Move
hdfs dfs -du -h <path>                  # Disk usage
hdfs dfs -chmod 755 <path>              # Change permissions
hdfs dfs -chown user:group <path>       # Change owner
hdfs dfsadmin -report                   # Cluster report
hdfs fsck / -files -blocks              # File system check
```

### MapReduce Commands

```bash
# Run example
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
  <example> <input> <output>

# WordCount
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
  wordcount /input /output

# List examples
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar
```

### YARN Commands

```bash
yarn application -list                          # List apps
yarn application -status <app-id>               # App status
yarn application -kill <app-id>                 # Kill app
yarn node -list                                 # List nodes
yarn node -status <node-id>                     # Node status
yarn logs -applicationId <app-id>               # View logs
```

### Administration Commands

```bash
hdfs dfsadmin -safemode get                     # Check safe mode
hdfs dfsadmin -safemode leave                   # Leave safe mode
hdfs balancer                                   # Balance cluster
hdfs namenode -format                           # Format NameNode
```

---

## Architecture Overview

### HDFS Architecture

```
Client → NameNode (metadata)
      → DataNodes (actual data blocks)
```

**Key Points**:
- NameNode: Master, stores metadata
- DataNodes: Workers, store data blocks
- Block size: 128MB default
- Replication: 3x default (1x for single node)
- Heartbeat: Every 3 seconds

### YARN Architecture

```
Client → ResourceManager → ApplicationMaster → NodeManagers
```

**Key Points**:
- ResourceManager: Master, schedules resources
- NodeManagers: Workers, run containers
- ApplicationMaster: Coordinates application tasks
- Container: Unit of resource allocation

---

## Performance Tips

### Single Node Optimization

1. **Increase Memory** (yarn-site.xml)
   ```xml
   <property>
       <name>yarn.nodemanager.resource.memory-mb</name>
       <value>4096</value>
   </property>
   ```

2. **Increase Virtual Cores**
   ```xml
   <property>
       <name>yarn.nodemanager.resource.cpu-vcores</name>
       <value>4</value>
   </property>
   ```

3. **Disable Memory Checks** (for development)
   ```xml
   <property>
       <name>yarn.nodemanager.pmem-check-enabled</name>
       <value>false</value>
   </property>
   ```

### Cluster Optimization

1. **Adjust Replication**
   ```xml
   <property>
       <name>dfs.replication</name>
       <value>3</value>  <!-- For 3+ nodes -->
   </property>
   ```

2. **Block Size**
   ```xml
   <property>
       <name>dfs.blocksize</name>
       <value>134217728</value>  <!-- 128MB -->
   </property>
   ```

---

## Learning Resources

### Documentation
- Apache Hadoop Docs: https://hadoop.apache.org/docs/
- HDFS Architecture: https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html
- YARN Architecture: https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html
- MapReduce Tutorial: https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html

### Books
- "Hadoop: The Definitive Guide" by Tom White
- "Data-Intensive Text Processing with MapReduce"

### Online Courses
- Coursera: Big Data Specialization
- Udemy: Apache Hadoop courses
- edX: Big Data courses

---

## Next Steps

1. ✅ **Complete Installation**
   ```bash
   ./hadoop-master.sh  # Select option 1
   ```

2. ✅ **Learn HDFS**
   ```bash
   ./hadoop-master.sh  # Select option 7, then 1
   ```

3. ✅ **Try MapReduce**
   ```bash
   ./hadoop-master.sh  # Select option 7, then 2
   ```

4. ✅ **Setup Database**
   ```bash
   ./hadoop-master.sh  # Select option 2
   ```

5. ✅ **Explore Web UIs**
   ```bash
   ./hadoop-master.sh  # Select option 5
   ```

6. ➡ **Build Real Projects**
   - Log analysis
   - Data warehousing
   - ETL pipelines
   - Machine learning

---

## Support & Contribution

### Issues
Report bugs or ask questions by opening an issue.

### Contributing
Contributions welcome! Feel free to:
- Add more examples
- Improve documentation
- Fix bugs
- Share your learnings

---

## License

Educational/Learning purposes

---

## Credits

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  ★🔥 Crafted with ♥ by devnolife 🔥★                     ║
║                                                           ║
║  github.com/devnolife                                     ║
║                                                           ║
║  Version: 1.0                                             ║
║  Date: 2025-11-04                                         ║
║                                                           ║
║  "Big Data never sleeps... Keep Hadooping!" 🚀           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

**Happy Hadooping!** 🚀

For quick help, just run:
```bash
./hadoop-master.sh
```
