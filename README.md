# Big Data Ingestion Pipeline

## Overview

This project implements a containerized Big Data ingestion platform built with Apache NiFi, Apache Airflow, Hadoop HDFS, Hive, MySQL, and LDAP authentication.

The platform supports ingesting data from multiple sources (flat files and relational databases), converts supported formats into a common CSV representation, stores the data in HDFS using a partitioned directory structure, and orchestrates the entire workflow with Apache Airflow.

The project follows a modular architecture inspired by production data engineering pipelines, emphasizing maintainability, scalability, and separation of responsibilities.

---

# Architecture

```
                   +----------------+
                   |  Input Files   |
                   | CSV JSON XML   |
                   | TXT (Delimited)|
                   +--------+-------+
                            |
                            |
                            v
                  +-------------------+
                  | File Ingestion PG |
                  +-------------------+
                            |
                            |
                            +----------------------+
                                                   |
                                                   |
                  +-------------------+            |
                  | JDBC Ingestion PG |------------+
                  +-------------------+
                            |
                            v
                    Unified CSV Output
                            |
                            v
                    +----------------+
                    |   Storage PG   |
                    |    PutHDFS     |
                    +----------------+
                            |
                            v
                    Hadoop HDFS
                            |
                            v
                         Apache Hive


               +-----------------------------+
               |       Apache Airflow        |
               |-----------------------------|
               | • Starts required services  |
               | • Waits for dependencies    |
               | • Launches NiFi pipeline    |
               | • Runtime monitoring        |
               | • Discord notifications     |
               +-----------------------------+


            +-------------------------------+
            |            LDAP               |
            |  NiFi Authentication         |
            +-------------------------------+
```

---

# Technologies

- Apache NiFi
- Apache Airflow
- Hadoop HDFS
- Apache Hive
- MySQL
- OpenLDAP
- phpLDAPadmin
- phpMyAdmin
- Docker & Docker Compose
- Python

---

# Features

## Data Sources

- Flat file ingestion
- JDBC incremental ingestion

## Supported Formats

- CSV
- JSON
- XML
- Delimited Text (.txt)

All supported formats are converted into a unified CSV format before storage.

---

## Storage

Files are stored inside HDFS using dynamic partitions.

Example:

```
/data/csv_source/customers/
    year=2026/
        month=07/
            day=20/
```

The destination path is generated automatically using NiFi Expression Language.

---

## NiFi Architecture

```
Main Pipeline

├── Sources
│   ├── File Ingestion
│   │   ├── CSV
│   │   ├── JSON
│   │   ├── XML
│   │   └── TXT
│   │
│   └── JDBC Ingestion
│
├── Storage
│   └── PutHDFS
│
├── Error Handling
│   ├── Failed Fetch
│   ├── Retry Exceeded
│   └── Unsupported Files
│
└── Monitoring (ready for future extensions)
```

---

## Airflow

Airflow orchestrates the pipeline by:

- Starting required Docker containers
- Waiting until each service is reachable
- Authenticating with NiFi using LDAP
- Launching the ingestion Process Group
- Sending Discord success/failure notifications
- Reporting pipeline runtime

---

## Authentication

NiFi authentication is delegated to OpenLDAP.

phpLDAPadmin is used to manage LDAP users through a web interface.

Credentials are managed securely using Airflow Variables instead of hardcoded values.

---

# Project Structure

```
bigdata-ingestion-pipeline/

├── airflow/
│   └── dags/
│       ├── final_ingestion_pipeline.py
│       └── utils/
│           ├── docker_utils.py
│           ├── nifi_utils.py
│           ├── notify_utils.py
│           └── wait_utils.py
│
├── data/
│   ├── input/
│   ├── output/
│   ├── quarantine/
│   └── archive/
│
├── hadoop/
│   ├── config/
│   ├── namenode/
│   └── datanode/
│
├── hive/
│   └── jdbc/
│
├── nifi/
│   ├── conf/
│   ├── extensions/
│   └── jdbc/
│
├── docker-compose.yml
└── README.md
```

---

# Workflow

```
Input File / Database
          │
          ▼
 File or JDBC Ingestion
          │
          ▼
 Format Conversion
(JSON/XML/TXT → CSV)
          │
          ▼
Metadata Enrichment
          │
          ▼
 Error Handling
          │
          ▼
      PutHDFS
          │
          ▼
        HDFS
          │
          ▼
        Hive
```

---

# Docker Services

The project includes the following services:

- Apache NiFi
- Apache Airflow
- PostgreSQL (Airflow Metadata)
- Hadoop NameNode
- Hadoop DataNode
- Apache Hive
- MySQL
- phpMyAdmin
- OpenLDAP
- phpLDAPadmin

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/sunyata0-0/BigData-Ingestion-Pipeline/tree/main
cd bigdata-ingestion-pipeline
```

Start the environment:

```bash
docker compose up -d
```

Open the web interfaces:

| Service | URL |
|----------|-----|
| NiFi | https://localhost:8444 |
| Airflow | http://localhost:8082 |
| phpMyAdmin | http://localhost:8081 |
| phpLDAPadmin | https://localhost:8085 |
| NameNode UI | http://localhost:9870 |

Trigger the Airflow DAG:

```
final_ingestion_pipeline
```

The DAG will automatically:

1. Start required containers (if necessary)
2. Wait for service readiness
3. Authenticate to NiFi
4. Launch the ingestion Process Group
5. Send a Discord notification with the execution summary

---

# Future Improvements

- Dedicated Monitoring Process Group
- Centralized NiFi logging
- Email notifications
- Parquet and Avro support
- Kafka ingestion
- Spark processing layer
- Automated Hive table creation
- Data quality validation

---

# Author

**Mahdi Benhamadi**

Engineering Student — Data Science, Big Data & Artificial Intelligence

Internship Project — Big Data Ingestion Pipeline