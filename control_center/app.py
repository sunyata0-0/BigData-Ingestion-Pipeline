from flask import Flask

from blueprints.dashboard import dashboard_bp
from blueprints.upload import upload_bp
from blueprints.airflow import airflow_bp
from blueprints.docker import docker_bp

app = Flask(__name__)

app.config.from_pyfile("config.py")

app.register_blueprint(dashboard_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(airflow_bp)
app.register_blueprint(docker_bp)

if __name__ == "__main__":
    app.run(debug=False)