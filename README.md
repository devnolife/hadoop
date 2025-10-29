# Hadoop - Teknologi Big Data

Kumpulan script Python untuk operasi Hadoop dan HDFS.

## 📋 Daftar Script

### 1. `hadoop_setup.py`
Setup dan konfigurasi Hadoop untuk Windows.
- ✅ Instalasi Hadoop Setup Single Node
- ✅ Setup Cluster
- ✅ Menjalankan perintah dasar Hadoop

**Cara Menjalankan:**
```bash
python hadoop_setup.py
```

### 2. `hdfs_operations.py`
Operasi HDFS (Hadoop Distributed File System).
- ✅ Menjalankan perintah dasar Hadoop
- ✅ Mengambil data dari HDFS (get)
- ✅ Memasukkan data ke HDFS (put)

**Cara Menjalankan:**
```bash
python hdfs_operations.py
```

**Contoh Penggunaan:**
```python
from hdfs_operations import HDFSOperations

hdfs = HDFSOperations()

# Upload file
hdfs.upload_file('data.txt', '/user/hadoop/input/data.txt')

# Download file
hdfs.download_file('/user/hadoop/output/result.txt', 'result.txt')

# List directory
hdfs.list_directory('/user/hadoop')
```

### 3. `database_to_hdfs.py`
Memasukkan data dari database ke HDFS.
- ✅ Export dari MySQL ke CSV
- ✅ Export dari PostgreSQL ke CSV
- ✅ Upload ke HDFS
- ✅ Integration dengan Apache Sqoop

**Cara Menjalankan:**
```bash
python database_to_hdfs.py
```

**Contoh Penggunaan:**
```python
from database_to_hdfs import DatabaseToHDFS

db_to_hdfs = DatabaseToHDFS()

# MySQL ke HDFS
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'mydb'
}

db_to_hdfs.mysql_to_hdfs(
    db_config=mysql_config,
    table='customers',
    hdfs_path='/user/hadoop/data/customers.csv'
)
```

### 4. `hadoop_commands.py`
Panduan lengkap perintah dasar Hadoop.
- ✅ File operations
- ✅ Data transfer
- ✅ Information & monitoring
- ✅ Permissions
- ✅ Admin commands
- ✅ MapReduce commands

**Cara Menjalankan:**
```bash
python hadoop_commands.py
```

## 🔧 Prerequisites

### Windows
1. **Java JDK 8 atau lebih tinggi**
   ```bash
   java -version
   ```

2. **Hadoop**
   - Download dari: https://hadoop.apache.org/releases.html
   - Extract ke direktori (misal: C:\hadoop)
   - Set environment variables:
     - `HADOOP_HOME=C:\hadoop`
     - `JAVA_HOME=C:\Program Files\Java\jdk-xx`
     - Tambahkan ke PATH: `%HADOOP_HOME%\bin`

3. **Python Libraries**
   ```bash
   pip install mysql-connector-python    # Untuk MySQL
   pip install psycopg2-binary          # Untuk PostgreSQL
   ```

## 📝 Tugas yang Dicakup

1. ✅ **Instalasi Hadoop Setup Single Node**
2. ✅ **Setup Cluster**
3. ✅ **Menjalankan perintah dasar Hadoop**
4. ✅ **Melentikkan dan mengambil data dari HDFS**
5. ✅ **Memasukkan data dari database ke HDFS**

## 🚀 Quick Start

1. **Format NameNode (pertama kali)**
   ```bash
   hdfs namenode -format
   ```

2. **Start Hadoop**
   ```bash
   start-all.sh    # Linux/Mac
   # atau
   start-dfs.cmd   # Windows
   start-yarn.cmd  # Windows
   ```

3. **Verifikasi**
   - NameNode: http://localhost:9870
   - ResourceManager: http://localhost:8088
   - DataNode: http://localhost:9864

4. **Test HDFS**
   ```bash
   hdfs dfs -mkdir -p /user/hadoop/test
   hdfs dfs -ls /
   ```

## 📚 Referensi

- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/)
- [HDFS Commands Guide](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html)
- [Hadoop on Windows](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)

## 💡 Tips

- Pastikan port yang diperlukan tidak terblokir (9870, 8088, 9864)
- Gunakan absolute path saat bekerja dengan HDFS
- Backup data sebelum format NameNode
- Monitor disk space di DataNode

## 🐛 Troubleshooting

**Problem: Command not found**
- Pastikan HADOOP_HOME sudah di-set
- Pastikan %HADOOP_HOME%\bin ada di PATH

**Problem: Connection refused**
- Cek apakah Hadoop services sudah running
- Verifikasi dengan: `jps` (Java Process Status)

**Problem: Permission denied**
- Cek permission file di HDFS: `hdfs dfs -ls -R /`
- Change permission: `hdfs dfs -chmod 777 /path`

## 📧 Kontak

Untuk pertanyaan atau bantuan, silakan hubungi dosen atau asisten mata kuliah.

---
**Teknologi Big Data - Semester 2**
