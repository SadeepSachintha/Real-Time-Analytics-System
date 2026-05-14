#!/bin/bash

echo "Submitting Spark Job to Docker container..."

docker exec -it \
  -e KAFKA_HOST=kafka \
  -e POSTGRES_HOST=postgres \
  real-time-analytics-system-spark-master-1 spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2 \
  /opt/bitnami/spark/app/processor.py
