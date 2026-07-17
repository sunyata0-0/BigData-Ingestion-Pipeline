from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import urllib3

# Disable warnings for NiFi's self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def start_nifi():

    BASE = "https://nifi:8443"
    USERNAME = "mahdi"
    PASSWORD = "mahdi2003,///"

    PROCESS_GROUP_ID = "6bf95b17-019f-1000-de47-473494322749"

    # Login and get JWT token
    response = requests.post(
        f"{BASE}/nifi-api/access/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "username": USERNAME,
            "password": PASSWORD,
        },
        verify=False,
    )

    response.raise_for_status()

    token = response.text

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Start the process group
    response = requests.put(
        f"{BASE}/nifi-api/flow/process-groups/{PROCESS_GROUP_ID}",
        headers=headers,
        json={
            "id": PROCESS_GROUP_ID,
            "state": "RUNNING"
        },
        verify=False,
    )

    response.raise_for_status()

    print("NiFi process group started successfully!")


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

    run_nifi = PythonOperator(
        task_id="run_nifi_pipeline",
        python_callable=start_nifi,
    )

    finished = BashOperator(
        task_id="pipeline_finished",
        bash_command='echo "Pipeline launched successfully!"'
    )

    (
        check_input
        >> check_mysql
        >> check_hdfs
        >> check_nifi
        >> run_nifi
        >> finished
    )
