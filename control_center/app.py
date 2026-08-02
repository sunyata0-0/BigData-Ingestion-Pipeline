from flask import Flask

from blueprints.dashboard import dashboard_bp
from blueprints.upload import upload_bp
from blueprints.airflow import airflow_bp
from blueprints.docker import docker_bp
from blueprints.ldap import ldap_bp
from blueprints.hdfs import hdfs_bp
from blueprints.hive import hive_bp
from blueprints.mysql_routes import mysql_bp, init_mysql
from blueprints.discord import discord_bp




app = Flask(__name__)

app.config.from_pyfile("config.py")

init_mysql(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(airflow_bp)
app.register_blueprint(docker_bp)
app.register_blueprint(ldap_bp)
app.register_blueprint(hdfs_bp)
app.register_blueprint(hive_bp)
app.register_blueprint(mysql_bp, url_prefix="/mysql")
app.register_blueprint(discord_bp)

if __name__ == "__main__":
    app.run(debug=False)