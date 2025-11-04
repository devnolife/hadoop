#!/bin/bash
# Script untuk memulai Hadoop Services

echo "=== Starting Hadoop Services ==="

# Source environment variables
source /home/devnolife/hdoop/scripts/env-setup.sh

# Start HDFS
echo "Starting HDFS..."
$HADOOP_HOME/sbin/start-dfs.sh

# Wait a bit
sleep 5

# Start YARN
echo "Starting YARN..."
$HADOOP_HOME/sbin/start-yarn.sh

# Wait a bit
sleep 5

# Check if services are running
echo ""
echo "=== Checking Services ==="
jps

echo ""
echo "=== Web Interfaces ==="
echo "NameNode UI: http://localhost:9870"
echo "ResourceManager UI: http://localhost:8088"
echo "DataNode UI: http://localhost:9864"
