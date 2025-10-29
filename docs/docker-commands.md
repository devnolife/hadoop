# Hadoop Docker Commands

## Quick Reference

### Start/Stop Cluster

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f
```

### Check Status

```bash
# Check running containers
docker-compose ps

# Check specific service
docker logs namenode
docker logs datanode
docker logs resourcemanager
```

### HDFS Commands

```bash
# List root directory
docker exec -it namenode hdfs dfs -ls /

# Create directory
docker exec -it namenode hdfs dfs -mkdir -p /user/data

# Upload file
docker cp sample.txt namenode:/tmp/
docker exec -it namenode hdfs dfs -put /tmp/sample.txt /user/data/

# Download file
docker exec -it namenode hdfs dfs -get /user/data/sample.txt /tmp/
docker cp namenode:/tmp/sample.txt ./downloaded.txt

# View file content
docker exec -it namenode hdfs dfs -cat /user/data/sample.txt

# Remove file
docker exec -it namenode hdfs dfs -rm /user/data/sample.txt

# Disk usage
docker exec -it namenode hdfs dfs -du -h /user/data
```

### Interactive Shell

```bash
# Enter namenode container
docker exec -it namenode bash

# Enter datanode container
docker exec -it datanode bash

# Inside container, run HDFS commands
hdfs dfs -ls /
hdfs dfs -mkdir /test
hdfs dfsadmin -report
```

### Web UIs

Access these URLs in your browser:

- **NameNode**: http://localhost:9870
- **ResourceManager**: http://localhost:8088
- **HistoryServer**: http://localhost:8188

### Troubleshooting

```bash
# Restart specific service
docker-compose restart namenode

# View detailed logs
docker logs namenode --tail 100

# Check container resource usage
docker stats

# Remove all stopped containers
docker container prune

# Remove unused volumes
docker volume prune
```

### Advanced Operations

```bash
# Execute Python script in container
docker exec -it namenode python /path/to/script.py

# Copy directory to container
docker cp ./local_dir namenode:/tmp/

# Export container logs
docker logs namenode > namenode.log 2>&1

# Check HDFS health
docker exec -it namenode hdfs fsck /
```
