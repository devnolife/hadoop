#!/bin/bash
# HDFS Basic Commands Example

# Source environment
source /home/devnolife/hdoop/scripts/env-setup.sh

echo "=== HDFS Basic Commands Demo ==="

echo -e "\n1. Create directory in HDFS"
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -mkdir -p /user/hadoop/output

echo -e "\n2. List HDFS root directory"
hdfs dfs -ls /

echo -e "\n3. Upload file to HDFS"
hdfs dfs -put /home/devnolife/hdoop/data/input/sample-data.txt /user/hadoop/input/

echo -e "\n4. List files in HDFS"
hdfs dfs -ls /user/hadoop/input/

echo -e "\n5. View file content in HDFS"
hdfs dfs -cat /user/hadoop/input/sample-data.txt

echo -e "\n6. Get file from HDFS"
hdfs dfs -get /user/hadoop/input/sample-data.txt /home/devnolife/hdoop/data/output/downloaded-file.txt

echo -e "\n7. Check file size"
hdfs dfs -du -h /user/hadoop/input/

echo -e "\n8. Check HDFS disk usage"
hdfs dfs -df -h

echo -e "\n9. Copy file within HDFS"
hdfs dfs -cp /user/hadoop/input/sample-data.txt /user/hadoop/input/sample-data-copy.txt

echo -e "\n10. Remove file from HDFS"
hdfs dfs -rm /user/hadoop/input/sample-data-copy.txt

echo -e "\n=== Demo Complete ==="
