#!/bin/bash
# Import data from MySQL to HDFS using Sqoop
# Prerequisites: MySQL and Sqoop must be installed

# Source environment
source /home/devnolife/hdoop/scripts/env-setup.sh

echo "=== MySQL to HDFS Import Example ==="

# Database configuration
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="testdb"
DB_USER="root"
DB_PASSWORD="password"
DB_TABLE="users"

echo -e "\n1. Testing MySQL connection..."
# Note: This requires MySQL client to be installed
# mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e "SELECT 1"

echo -e "\n2. Import table from MySQL to HDFS using Sqoop..."
# Note: This requires Sqoop to be installed and configured
# sqoop import \
#   --connect jdbc:mysql://$DB_HOST:$DB_PORT/$DB_NAME \
#   --username $DB_USER \
#   --password $DB_PASSWORD \
#   --table $DB_TABLE \
#   --target-dir /user/hadoop/sqoop/import/$DB_TABLE \
#   --m 1

echo -e "\n3. Verify imported data..."
# hdfs dfs -ls /user/hadoop/sqoop/import/$DB_TABLE
# hdfs dfs -cat /user/hadoop/sqoop/import/$DB_TABLE/part-m-00000

echo -e "\nNote: This is a template script."
echo "To use this script:"
echo "1. Install MySQL: sudo apt install mysql-server mysql-client"
echo "2. Download and configure Sqoop"
echo "3. Create sample database and table"
echo "4. Update connection details in this script"
echo "5. Install MySQL JDBC driver in Sqoop lib directory"

cat << 'EOF'

=== Sample MySQL Database Setup ===

-- Create database
CREATE DATABASE testdb;
USE testdb;

-- Create sample table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email) VALUES
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com'),
('Bob Johnson', 'bob@example.com');

EOF
