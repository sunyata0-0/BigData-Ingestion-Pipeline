from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from services.upload_services import UploadService


upload_bp = Blueprint(
    "upload",
    __name__
)

@upload_bp.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:

        return jsonify({

            "success": False,
            "message": "No file provided."

        }), 400


    file = request.files["file"]

    service = UploadService(
        current_app.config["UPLOAD_FOLDER"]
    )

    success, message = service.save(file)

    status = 200 if success else 400

    return jsonify({

        "success": success,
        "message": message

    }), status