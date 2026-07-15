from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ingestion_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@hourly",
    catchup=False,
    tags=["nifi", "hdfs", "mysql"],
) as dag:

    check_input = BashOperator(
        task_id="check_input_folder",
        bash_command="""
        test -d /opt/airflow/data/input
        """
    )

    check_mysql = BashOperator(
        task_id="check_mysql",
        bash_command="""
        nc -z mysql 3306
        """
    )

    '''check_hdfs = BashOperator(
        task_id="check_hdfs",
        bash_command="""
        hdfs dfs -test -d /data/raw
        """
    )'''
    
    check_hdfs = BashOperator(
        task_id="check_hdfs",
        bash_command="""
        nc -z namenode 9000
        """
    )

    check_nifi = BashOperator(
        task_id="check_nifi",
        bash_command="""
        nc -z nifi 8443
        """
    )

    finished = BashOperator(
        task_id="pipeline_ready",
        bash_command='echo "Everything is healthy. NiFi is ready to ingest data."'
    )

    (
        check_input
        >> check_mysql
        >> check_hdfs
        >> check_nifi
        >> finished
    )