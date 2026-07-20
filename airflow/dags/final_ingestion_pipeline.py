from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

from datetime import datetime
import time

from utils.docker_utils import (
    start_container,
    container_summary,
)

from utils.wait_utils import (
    wait_for_port,
    wait_until,
)

from utils.nifi_utils import (
    run_pipeline,
    process_group_running,
)

from utils.notify_utils import (
    notify_success,
    notify_failure,
    build_summary,
)


#PROCESS_GROUP_ID = "6bf95b17-019f-1000-de47-473494322749"
process_group = Variable.get("nifi_process_group_id")

CONTAINERS = [
    "mysql",
    "namenode",
    "datanode",
    "ldap",
    "phpldapadmin",
    "phpmyadmin",
    "hive",
    "nifi",
]

PORTS = {
    "mysql": 3306,
    "namenode": 9000,
    "ldap": 389,
    "hive": 10000,
    "nifi": 8443,
}


def run_ingestion_pipeline():

    start = time.time()

    webhook = Variable.get("discord_webhook")
    username = Variable.get("nifi_username")
    password = Variable.get("nifi_password")

    try:

        # -----------------------------
        # Start required containers
        # -----------------------------

        missing = []

        for container in CONTAINERS:
            result = start_container(container)

            if result["status"] == "missing":
                missing.append(container)

        if missing:
            raise RuntimeError(
                f"Missing containers: {', '.join(missing)}"
            )

        # -----------------------------
        # Wait until services are ready
        # -----------------------------

        for service, port in PORTS.items():
            wait_for_port(service, port)

        # -----------------------------
        # Login & start NiFi
        # -----------------------------

        token = run_pipeline(
            process_group,
            username,
            password,
        )

        wait_until(
            lambda: process_group_running(
                process_group,
                token,
            ),
            timeout=120,
            interval=3,
        )

        runtime = time.time() - start

        notify_success(
            webhook,
            build_summary(
                runtime,
                container_summary(CONTAINERS),
                process_group,
            ),
        )

    except Exception as e:

        runtime = time.time() - start

        notify_failure(
            webhook,
            f"""
Runtime:
{runtime:.1f}s

Reason:
{type(e).__name__}

{e}
""",
        )

        raise


with DAG(
    dag_id="final_ingestion_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@hourly",
    catchup=False,
    tags=["nifi", "hdfs", "mysql", "ldap"],
) as dag:

    run = PythonOperator(
        task_id="run_ingestion_pipeline",
        python_callable=run_ingestion_pipeline,
    )