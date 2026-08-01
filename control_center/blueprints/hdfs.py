from flask import Blueprint
from flask import jsonify
from flask import request

from services.hdfs_services import HDFSService

hdfs_bp = Blueprint(
    "hdfs",
    __name__,
    url_prefix="/hdfs"
)


@hdfs_bp.route("/list")
def list_hdfs():

    path = request.args.get("path", "/")

    service = HDFSService()

    success, data = service.list_directory(path)

    if success:

        return jsonify(data)

    return jsonify({
        "error": data
    }), 500