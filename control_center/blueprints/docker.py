from flask import (
    Blueprint,
    jsonify
)

from services.docker_services import DockerService


docker_bp = Blueprint(
    "docker",
    __name__,
    url_prefix="/docker"
)


@docker_bp.route("/status")
def status():

    service = DockerService()

    return jsonify(
        service.get_status()
    )


@docker_bp.route("/restart/<service>", methods=["POST"])
def restart(service):

    docker = DockerService()

    success, message = docker.restart_service(
        service
    )

    status_code = 200 if success else 400

    return jsonify({

        "success": success,
        "message": message

    }), status_code