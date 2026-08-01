from flask import (
    Blueprint,
    jsonify,
    current_app
)

from services.airflow_services import AirflowService


airflow_bp = Blueprint(
    "airflow",
    __name__
)


@airflow_bp.route("/airflow/run", methods=["POST"])
def run_workflow():

    service = AirflowService(

        current_app.config["AIRFLOW_URL"],
        current_app.config["AIRFLOW_USERNAME"],
        current_app.config["AIRFLOW_PASSWORD"]

    )

    success, message = service.trigger_dag(

        current_app.config["DAG_ID"]

    )

    return jsonify({

        "success": success,
        "message": message

    }), 200 if success else 400