# Big Data Ingestion Pipeline

## Overview

This project implements an end-to-end Big Data ingestion pipeline using Apache NiFi, Apache Airflow, Hadoop HDFS, Hive, and MySQL.

The pipeline automatically ingests CSV files, validates them, stores them in HDFS using a partitioned directory structure, updates Hive metadata, and orchestrates the entire workflow with Airflow.

The goal of this project is to demonstrate a production-inspired data ingestion architecture that is modular, scalable, and easy to maintain.

---

# Architecture

```
                CSV Files
                     │
                     ▼
               Apache NiFi
                     │
     ┌───────────────┼────────────────┐
     │               │                │
 Validation      Error Handling    Logging
     │
     ▼
 HDFS (Partitioned Storage)
     │
     ▼
 Apache Hive (External Tables)
     │
 Metadata stored in MySQL
     │
     ▼
 SQL Analytics

Apache Airflow
      │
      └── Orchestrates the entire pipeline
```

---

# Technologies

* Apache NiFi
* Apache Airflow
* Apache Hive
* Hadoop HDFS
* MySQL
* Docker & Docker Compose
* Python

---

# Features

* Automated CSV ingestion
* Validation of incoming files
* Invalid file quarantine
* Dynamic HDFS partitioning

```
/data/csv_source/customers/
    year=YYYY/
        month=MM/
            day=DD/
```

* Automatic Hive partition discovery
* External Hive tables
* Persistent Hive Metastore using MySQL
* Airflow DAG orchestration
* Modular NiFi Process Groups
* Parameterized NiFi configuration
* Dockerized deployment

---

# Project Structure

```
bigdata-ingestion-pipeline/

├── airflow/
│   └── dags/
│       └── ingestion_pipeline.py
│
├── hadoop/
│   └── config/
│
├── hive/
│   └── jdbc/
│
├── input/
├── output/
├── quarantine/
│
├── docker-compose.yml
└── README.md
```

---

# Workflow

1. A CSV file is placed into the input directory.
2. NiFi validates the file.
3. Invalid files are moved to the quarantine folder.
4. Valid files are uploaded to HDFS.
5. Files are stored using the following partition structure:

```
year=YYYY/month=MM/day=DD/
```

6. Airflow executes:

* Hive partition refresh

```
MSCK REPAIR TABLE customers;
```

7. Data becomes immediately available for SQL queries in Hive.

---

# Hive

The project uses an **External Hive Table**.

The table metadata is stored inside a dedicated MySQL Hive Metastore, while the actual data remains in HDFS.

Example queries:

```sql
SHOW TABLES;

SHOW PARTITIONS customers;

SELECT * FROM customers;

SELECT COUNT(*) FROM customers;

SELECT *
FROM customers
WHERE year='2026'
AND month='07'
AND day='16';
```

---

# Running the Project

Start all services:

```bash
docker compose up -d
```

Stop all services:

```bash
docker compose down
```

Start only Hive:

```bash
docker compose up -d hive
```

Open Hive:

```bash
docker exec -it hive beeline -u jdbc:hive2://localhost:10000/
```

---

# Future Improvements

* Email notifications from Airflow
* Enhanced error handling
* Detailed logging Process Group
* User authentication and authorization in NiFi
* Monitoring and alerting
* Support for additional data formats (JSON, Parquet, Avro)

---

# Author

Mahdi Benhamadi

Engineering Student – Data Science, Big Data & Artificial Intelligence

Internship Project – Big Data Ingestion Pipeline
