#!/bin/bash
# Hadoop Environment Setup Script

# Set JAVA_HOME
export JAVA_HOME=/home/devnolife/hdoop/jdk-11.0.2
export PATH=$JAVA_HOME/bin:$PATH

# Set HADOOP_HOME (will be set after Hadoop installation)
export HADOOP_HOME=/home/devnolife/hdoop/hadoop/hadoop-3.3.6
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"

# Display environment info
echo "=== Environment Setup ==="
echo "JAVA_HOME: $JAVA_HOME"
echo "HADOOP_HOME: $HADOOP_HOME"
echo "Java Version:"
java -version

echo ""
echo "To apply these settings, run: source scripts/env-setup.sh"
