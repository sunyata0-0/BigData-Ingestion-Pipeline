# Flask
SECRET_KEY = "bigdata-dashboard"

# URLs
NIFI_URL = "http://localhost:8443"
AIRFLOW_URL = "http://localhost:8080"
HDFS_URL = "http://localhost:9870"

# MySQL
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "bigdata"

# Hive
HIVE_HOST = "localhost"
HIVE_PORT = 10000

# Upload folder
UPLOAD_FOLDER = "C:/Users/M-S-I/Desktop/internship/bigdata-ingestion-pipeline/data/input"

# Airflow
AIRFLOW_URL = "http://localhost:8082/api/v1"
AIRFLOW_USERNAME = "admin"
AIRFLOW_PASSWORD = "admin"
DAG_ID = "final_ingestion_pipeline"

# LDAP
LDAP_HOST = "ldap://localhost:389"
LDAP_BIND_DN = "cn=admin,dc=intern,dc=local"
LDAP_PASSWORD = "admin"
LDAP_BASE_DN = "ou=people,dc=intern,dc=local"