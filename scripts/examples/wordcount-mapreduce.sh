#!/bin/bash
# WordCount MapReduce Example

# Source environment
source /home/devnolife/hdoop/scripts/env-setup.sh

echo "=== WordCount MapReduce Example ==="

# Prepare input
echo -e "\n1. Upload input file to HDFS"
hdfs dfs -mkdir -p /user/hadoop/wordcount/input
hdfs dfs -put /home/devnolife/hdoop/data/input/word-count-input.txt /user/hadoop/wordcount/input/

echo -e "\n2. Run WordCount MapReduce job"
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoop/wordcount/input /user/hadoop/wordcount/output

echo -e "\n3. View results"
hdfs dfs -cat /user/hadoop/wordcount/output/part-r-00000

echo -e "\n4. Download results"
hdfs dfs -get /user/hadoop/wordcount/output /home/devnolife/hdoop/data/output/wordcount-result

echo -e "\n=== WordCount Complete ==="
