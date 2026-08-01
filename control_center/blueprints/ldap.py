from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
)

from services.ldap_services import LDAPService


ldap_bp = Blueprint(
    "ldap",
    __name__,
    url_prefix="/ldap"
)


def get_service():

    return LDAPService(
        server=current_app.config["LDAP_HOST"],
        port=current_app.config["LDAP_PORT"],
        bind_dn=current_app.config["LDAP_BIND_DN"],
        bind_password=current_app.config["LDAP_BIND_PASSWORD"],
        base_dn=current_app.config["LDAP_BASE_DN"],
        admin_password=current_app.config["LDAP_ADMIN_PASSWORD"],
        viewer_password=current_app.config["LDAP_VIEWER_PASSWORD"],
    )


@ldap_bp.get("/users")
def users():

    service = get_service()

    return jsonify(
        service.get_users()
    )


@ldap_bp.post("/passwords")
def passwords():

    service = get_service()

    data = request.get_json()

    password = data.get(
        "password",
        ""
    )

    if not service.verify_master_password(password):

        return (
            jsonify(
                {
                    "success": False,
                    "message": "Incorrect password."
                }
            ),
            401,
        )

    return jsonify(
        {
            "success": True,
            "passwords": service.get_passwords()
        }
    )