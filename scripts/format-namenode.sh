#!/bin/bash
# Format Hadoop NameNode

echo "=== Formatting Hadoop NameNode ==="

# Source environment
source /home/devnolife/hdoop/scripts/env-setup.sh

# Create necessary directories
mkdir -p /home/devnolife/hdoop/hadoop/data/namenode
mkdir -p /home/devnolife/hdoop/hadoop/data/datanode
mkdir -p /home/devnolife/hdoop/hadoop/tmp

# Format NameNode
echo "Formatting NameNode..."
hdfs namenode -format -force

echo ""
echo "=== NameNode Formatted Successfully ==="
echo "You can now start Hadoop services with: ./scripts/start-hadoop.sh"
