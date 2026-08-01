from flask import Blueprint, current_app, jsonify

from services.hive_services import HiveService


hive_bp = Blueprint(
    "hive",
    __name__,
    url_prefix="/hive"
)


def service():
    return HiveService(current_app.config)


@hive_bp.get("/databases")
def databases():

    return jsonify(service().databases())


@hive_bp.get("/tables")
def tables():

    return jsonify(service().tables())


@hive_bp.get("/schema")
def schema():

    return jsonify(service().schema())


@hive_bp.get("/preview")
def preview():

    return jsonify(service().preview())