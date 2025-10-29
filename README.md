# 🐘 Hadoop Python Toolkit

**Modern Web Interface untuk MySQL & Big Data Processing**

## 🌟 Features

- 🌐 Modern Web Interface - Beautiful UI dengan Bootstrap 5
- 🔌 MySQL Management - Real-time connection, browse tables
- 📊 Data Preview - View data dalam modal window
- 📥 CSV Export - One-click export tables
- 💻 SQL Query Executor - Execute custom queries

## ⚡ Quick Start

### Cara Tercepat

**Windows:**
```cmd
start-web.bat
```

**Linux/Mac:**
```bash
./start-web.sh
```

Buka browser: **http://localhost:5000**

### Manual Setup

```bash
# Install dependencies
pip install -r requirements-web.txt

# Run application
python app.py
```

## 📦 Installation

### Requirements

- Python 3.8+
- MySQL 5.7+
- 2GB RAM minimum

### Setup Steps

**1. Install Dependencies**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-web.txt
```

**2. Setup MySQL**
```sql
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2)
);
```

**3. Run Application**
```bash
python app.py
```

## 💻 Usage

### Web Interface
1. Buka http://localhost:5000
2. Isi MySQL connection form
3. Klik "Connect to MySQL"
4. Browse tables, export CSV

### Python API
```python
from src.mysql_handler import MySQLHandler

mysql = MySQLHandler(
    host='localhost',
    user='root',
    password='pass',
    database='test_db'
)
mysql.connect()
mysql.export_table_to_csv('products')
```

## 📁 Project Structure

```
hadoop-python-toolkit/
├── app.py                    # Flask application
├── templates/index.html      # Web interface
├── static/app.js            # Frontend JS
├── src/
│   └── mysql_handler.py     # MySQL operations
├── examples/
│   ├── mysql_to_csv.py      # CLI export
│   └── backup_database.py   # Backup tool
└── requirements-web.txt     # Dependencies
```

## 🔧 Configuration

Create `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=test_db
```

## 🐛 Troubleshooting

### Cannot connect to MySQL
```bash
mysql -u root -p
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
```

### Module not found
```bash
pip install -r requirements-web.txt
```

## 📚 API Reference

**MySQLHandler:**
- `connect()` - Connect to MySQL
- `get_tables()` - List tables
- `export_table_to_csv(table)` - Export to CSV
- `execute_query(sql)` - Run SQL

## 🎓 Use Cases

1. Data Export - MySQL → CSV
2. Database Backup - All tables → CSV
3. Quick Analysis - Preview & query
4. Automation - Python scripts

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Open Pull Request

## 📜 License

MIT License © 2025 devnolife

---

**Made with ❤️ by devnolife**
