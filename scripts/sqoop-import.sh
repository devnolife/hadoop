#!/bin/bash
source /home/devnolife/hdoop/hadoop/config/database-config.conf

# Import table to HDFS
sqoop import \
  --connect "${JDBC_URL}" \
  --username "${DB_USER}" \
  --password "${DB_PASSWORD}" \
  --table "${DB_TABLE}" \
  --target-dir "/user/hadoop/sqoop/${DB_TABLE}" \
  --m 1

# Verify
hdfs dfs -ls /user/hadoop/sqoop/${DB_TABLE}/
