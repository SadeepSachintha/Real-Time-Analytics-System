#!/bin/bash

echo "Starting Real-Time Analytics System on Linux..."

# Start Docker Containers (Try 'docker compose' then fallback to 'docker-compose')
if docker compose version > /dev/null 2>&1; then
    docker compose up -d
else
    docker-compose up -d
fi

echo "Waiting for services to start..."
sleep 15

# Install Python Dependencies (Use python3 -m pip for better compatibility)
python3 -m pip install -r requirements.txt

# Setup Database
python3 setup_db.py

echo "Infrastructure is ready."
echo "To start the producer: python3 producer.py"
echo "To start the processor: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2 processor.py"
echo "Grafana is at http://localhost:3000 (admin/admin)"
