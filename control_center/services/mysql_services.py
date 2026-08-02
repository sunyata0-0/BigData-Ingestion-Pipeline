import subprocess
from datetime import date


class MySQLService:

    def __init__(self, config):
        self.container = config["MYSQL_CONTAINER"]
        self.database = config["MYSQL_DATABASE"]
        self.table = config["MYSQL_TABLE"]
        self.user = config["MYSQL_USER"]
        self.password = config["MYSQL_PASSWORD"]


    def insert(
        self,
        first_name,
        last_name,
        department,
        salary
    ):

        today = date.today()

        hire_date = today.strftime("%Y-%m-%d")

        query = f"""
        INSERT INTO {self.table}
        (
            first_name,
            last_name,
            department,
            salary,
            hire_date
        )
        VALUES
        (
            '{first_name}',
            '{last_name}',
            '{department}',
            {salary},
            '{hire_date}'
        );
        """

        command = [
            "docker",
            "exec",
            self.container,
            "mysql",
            "-u",
            self.user,
            f"-p{self.password}",
            self.database,
            "-e",
            query
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return {
            "success": True,
            "message": "Row inserted successfully."
        }