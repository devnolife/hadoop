#!/bin/bash
# Script untuk menghentikan Hadoop Services

echo "=== Stopping Hadoop Services ==="

# Source environment variables
source /home/devnolife/hdoop/scripts/env-setup.sh

# Stop YARN
echo "Stopping YARN..."
$HADOOP_HOME/sbin/stop-yarn.sh

# Stop HDFS
echo "Stopping HDFS..."
$HADOOP_HOME/sbin/stop-dfs.sh

echo ""
echo "=== Services Stopped ==="
jps
