@echo off
echo Starting Real-Time Analytics System...

:: Check for Docker Compose version
docker compose version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set DOCKER_CMD=docker compose
) else (
    set DOCKER_CMD=docker-compose
)

echo Using %DOCKER_CMD%...
%DOCKER_CMD% up -d

echo Waiting for services to start (this may take a minute on first run)...
timeout /t 30 /nobreak

:: Install Python Dependencies
pip install -r requirements.txt

:: Setup Database
python setup_db.py

echo Infrastructure is ready.
echo To start the producer: python producer.py
echo To start the processor: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.postgresql:postgresql:42.7.2 processor.py
echo Grafana is at http://localhost:3000 (admin/admin)
