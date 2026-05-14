@echo off
echo Starting Real-Time Analytics System...

:: Start Docker Containers
docker-compose up -d

echo Waiting for services to start...
timeout /t 15

:: Install Python Dependencies
pip install -r requirements.txt

:: Setup Database
python setup_db.py

echo Infrastructure is ready.
echo To start the producer: python producer.py
echo To start the processor: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2 processor.py
echo Grafana is at http://localhost:3000 (admin/admin)
