# 📊 Real-Time Analytics System for Sri Lankan Market Data

A high-performance, scalable streaming data pipeline designed to process and visualize Sri Lankan market prices in real-time using **Apache Kafka**, **Apache Spark**, and **Grafana**.

![Architecture](https://img.shields.io/badge/Architecture-Streaming-blue)
![Tech](https://img.shields.io/badge/Tech-Kafka%20|%20Spark%20|%20Postgres-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🏗️ System Architecture

The system follows a classic Lambda/Streaming architecture, entirely containerized:

```mermaid
graph LR
    A[Producer: Manning Market Sim] -->|JSON Stream| B(Apache Kafka)
    B -->|Subscribe| C[Spark Master/Worker]
    C -->|30s Window Aggregation| D[(PostgreSQL)]
    D -->|Query| E[Grafana Dashboard]
```

1.  **Data Source**: Python producer simulating live price fluctuations at Colombo's Manning Market.
2.  **Ingestion Layer**: Confluent Kafka handles the high-throughput message stream.
3.  **Processing Layer**: Spark Structured Streaming (running in Docker) performs windowed aggregations.
4.  **Storage Layer**: PostgreSQL stores the processed analytics.
5.  **Visualization Layer**: Grafana provides real-time dashboards with pre-configured data sources.

---

## 🚀 Key Features

- **Fully Dockerized**: No need to install Spark or Kafka on your host machine.
- **Real-Time Streaming**: End-to-end latency of seconds.
- **Robust Processing**: Intelligent 30-second sliding windows.
- **Cross-Platform**: Optimized for both **Windows** and **Ubuntu**.
- **Auto-Provisioned**: Grafana comes pre-linked to the PostgreSQL database.

---

## 🛠️ Tech Stack

- **Broker**: Confluent Kafka & Zookeeper
- **Engine**: Apache Spark 3.5.0 (Master/Worker containers)
- **Database**: PostgreSQL
- **Viz**: Grafana
- **Language**: Python 3.x
- **Containerization**: Docker & Docker Compose

---

## 🌐 Network & Ports

The system is configured to avoid common port conflicts (e.g., with XAMPP or local Postgres):

| Service | Internal Port | External Port | URL |
| :--- | :--- | :--- | :--- |
| **Grafana** | 3000 | **3000** | [http://localhost:3000](http://localhost:3000) |
| **Spark Master** | 8080 | **8081** | [http://localhost:8081](http://localhost:8081) |
| **PostgreSQL** | 5432 | **5433** | `localhost:5433` |
| **Kafka (External)** | 29092 | **29092** | `localhost:29092` |

---

## 🚦 Getting Started

### 1. Initialize Infrastructure
Ensure Docker is running, then pull the images and start the containers:

**Windows (PowerShell):**
```powershell
./start.bat
```

**Ubuntu/Linux (Bash):**
```bash
chmod +x *.sh
./start.sh
```

### 2. One-Time Setup
Initialize the database schema:
```bash
python3 setup_db.py
```

---

## 🔧 Troubleshooting

### Spark Image "Not Found"
If you encounter an error pulling `bitnami/spark:3.5`, ensure your `docker-compose.yml` uses the `bitnamilegacy` repository as shown:
```yaml
image: bitnamilegacy/spark:3.5
```
*Note: Bitnami migrated community images to the legacy repository in late 2025.*

### Permission Denied (Linux/Windows)
If scripts fail to run, re-apply execute permissions:
```bash
chmod +x start.sh stop.sh submit_processor.sh
```
*Note: The Spark submission scripts are configured to run as `root` inside the container to avoid Ivy cache permission issues.*

### PostgreSQL Connection Issues
If the database container fails to start or rejects connections:
1. Ensure you are using `postgres:16` as defined in `docker-compose.yml`.
2. If you previously used a different version, you may need to clear the volume: `docker compose down -v`.

---

## 🔄 Daily Workflow

Once the setup is done, follow these steps to run the analytics:

1.  **Start Data Feed**:
    ```bash
    python3 producer.py
    ```
2.  **Submit Spark Job**:
    **Windows:**
    ```powershell
    ./submit_processor.bat
    ```
    **Linux:**
    ```bash
    ./submit_processor.sh
    ```
3.  **View Dashboard**:
    Open `http://localhost:3000` (admin/admin).

---

## 📁 Project Structure

```text
.
├── grafana/                # Grafana provisioning configs
├── docker-compose.yml      # Infrastructure (Kafka, Spark, Postgres, Grafana)
├── producer.py             # Kafka data producer (Market Simulator)
├── processor.py            # PySpark streaming logic
├── submit_processor.sh / .bat # Script to run Spark job in Docker
├── setup_db.py             # Database initialization (with retry logic)
├── requirements.txt        # Python dependencies
├── start.sh / .bat         # System startup scripts
└── stop.sh / .bat          # System shutdown scripts
```

---

## 👤 Author

**Sadeep Sachintha**
- GitHub: [@SadeepSachintha](https://github.com/SadeepSachintha)

---
*Developed as part of the Real-Time Analytics System project.*
