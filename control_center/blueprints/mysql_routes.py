from flask import Blueprint, request, jsonify

from services.mysql_services import MySQLService


mysql_bp = Blueprint("mysql", __name__)


def init_mysql(app):

    service = MySQLService(app.config)


    @mysql_bp.post("/insert")
    def insert():

        data = request.get_json()

        try:

            result = service.insert(
                data["first_name"],
                data["last_name"],
                data["department"],
                data["salary"]
            )

            return jsonify(result)

        except Exception as error:

            return jsonify({
                "success": False,
                "message": str(error)
            }), 500