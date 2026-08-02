# Big Data Ingestion Pipeline

## Overview

This project implements a containerized Big Data ingestion platform built with Apache NiFi, Apache Airflow, Hadoop HDFS, Apache Hive, MySQL, OpenLDAP, and a custom Flask-based Control Center.

The platform supports ingesting data from multiple sources (flat files and relational databases), converting supported formats into a unified CSV representation, storing data inside HDFS using partitioned directories, cataloging datasets with Hive, and orchestrating the entire workflow through Apache Airflow.

To simplify operation and monitoring, a lightweight web-based Control Center was developed during the internship. The dashboard provides a centralized interface for managing the platform without switching between multiple web interfaces.

---

# Architecture

```
                         +----------------------+
                         |   Flask Dashboard    |
                         +----------+-----------+
                                    |
        +-------------+-------------+-------------+-------------+
        |             |             |             |             |
        v             v             v             v             v
     Upload       Airflow        Docker         LDAP       Discord
        |             |             |             |             |
        +-------------+-------------+-------------+-------------+
                                    |
                                    v

                   +----------------+
                   |  Input Files   |
                   | CSV JSON XML   |
                   | TXT Delimited  |
                   +--------+-------+
                            |
                            |
                            v
                  +-------------------+
                  | File Ingestion PG |------------+
                  +-------------------+            |
                            ^                      |
                            |                      |
                  +-------------------+            |
                  | JDBC Ingestion PG |            |
                  +-------------------+            |
                                                   |
                            +----------------------+
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
            |      NiFi Authentication      |
            +-------------------------------+
```

---

# Technologies

* Apache NiFi
* Apache Airflow
* Hadoop HDFS
* Apache Hive
* MySQL
* OpenLDAP
* phpLDAPadmin
* phpMyAdmin
* Docker
* Docker Compose
* Flask
* Python

---

# Platform Features

## Data Sources

* Flat file ingestion
* JDBC incremental ingestion

## Supported Formats

* CSV
* JSON
* XML
* Delimited Text (.txt)

All supported formats are automatically converted into a unified CSV format before storage.

---

## Storage

Files are stored inside Hadoop HDFS using dynamic partition directories.

Example:

```text
/data/csv_source/customers/
    year=2026/
        month=07/
            day=20/
```

The destination path is generated dynamically using NiFi Expression Language.

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
└── Monitoring
```

---

## Airflow

Airflow orchestrates the entire platform by:

* Starting required Docker containers
* Waiting until every dependency becomes available
* Authenticating with NiFi using LDAP
* Launching the ingestion Process Group
* Sending Discord success/failure notifications
* Reporting total execution runtime

---

## Authentication

NiFi authentication is delegated to OpenLDAP.

phpLDAPadmin provides user management through a web interface.

Sensitive credentials are managed through Airflow Variables instead of hardcoded values.

---

# Control Center

A lightweight Flask dashboard providing a centralized interface for operating the entire platform.

Current features include:

* Upload files directly into the ingestion folder
* Trigger the Airflow workflow
* View Docker container status
* Start and stop Docker containers
* Browse LDAP users
* Browse HDFS directories
* Explore Hive databases
* Explore Hive tables
* View Hive table schemas
* Preview Hive table contents
* Insert new rows into the MySQL source database
* Send custom Discord notifications
* Display the NiFi pipeline diagram
* View project documentation from the dashboard

---

# Project Structure

```text
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
├── dashboard/
│   ├── blueprints/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── app.py
│
├── data/
│   ├── input/
│   ├── output/
│   ├── quarantine/
│   └── archive/
│
├── hadoop/
├── hive/
├── nifi/
├── docker-compose.yml
└── README.md
```

---

# Workflow

```text
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

The platform includes:

* Apache NiFi
* Apache Airflow
* PostgreSQL
* Hadoop NameNode
* Hadoop DataNode
* Apache Hive
* MySQL
* phpMyAdmin
* OpenLDAP
* phpLDAPadmin

---

# Running the Project

Clone the repository:

```bash
git clone https://github.com/sunyata0-0/BigData-Ingestion-Pipeline.git
cd BigData-Ingestion-Pipeline
```

Start the platform:

```bash
docker compose up -d
```

Run the Flask dashboard:

```bash
python app.py
```

---

## Web Interfaces

| Service      | URL                    |
| ------------ | ---------------------- |
| Dashboard    | http://localhost:5000  |
| NiFi         | https://localhost:8444 |
| Airflow      | http://localhost:8082  |
| phpMyAdmin   | http://localhost:8081  |
| phpLDAPadmin | https://localhost:8085 |
| NameNode UI  | http://localhost:9870  |

---

## Running the Pipeline

Trigger the Airflow DAG:

```text
final_ingestion_pipeline
```

The DAG automatically:

1. Starts required containers (if needed)
2. Waits for service readiness
3. Authenticates to NiFi
4. Launches the ingestion Process Group
5. Stores processed data in HDFS
6. Refreshes Hive metadata
7. Sends a Discord notification containing the execution summary

---

# Dashboard Preview

> Screenshots of the Control Center, Docker Manager, Hive Explorer, HDFS Browser, MySQL Insert, and Discord Notifications can be added here.

---

# Future Improvements

* Live pipeline monitoring
* Execution history
* Dashboard authentication
* Hive query editor
* Kafka ingestion
* Spark processing
* Parquet and Avro support
* Automatic Hive table creation
* Data quality validation

---

# Author

**Mahdi Benhamadi**

Engineering Student — Data Science, Big Data & Artificial Intelligence

Internship Project — Big Data Ingestion Pipeline
