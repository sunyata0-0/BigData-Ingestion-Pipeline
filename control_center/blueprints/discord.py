from flask import Blueprint, current_app, jsonify, request

from services.discord_services import DiscordService


discord_bp = Blueprint("discord", __name__)


@discord_bp.route("/discord/send", methods=["POST"])
def send_notification():

    data = request.get_json()

    message = data.get("message", "").strip()
    
    notification_type = data.get("type", "info")

    if not message:
        return jsonify({
            "success": False,
            "message": "Message cannot be empty."
        }), 400

    service = DiscordService(current_app.config)

    try:

        result = service.send(message,notification_type)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500