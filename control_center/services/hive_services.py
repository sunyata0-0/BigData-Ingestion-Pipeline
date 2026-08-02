import csv
import io
import subprocess


class HiveService:

    def __init__(self, config):
        self.container = config["HIVE_CONTAINER"]
        self.database = config["HIVE_DATABASE"]
        self.table = config["HIVE_TABLE"]


    def _run_query(self, query):

        command = [
            "docker",
            "exec",
            self.container,
            "beeline",
            "-u",
            "jdbc:hive2://localhost:10000",
            "--silent=true",
            "--outputformat=csv2",
            "-e",
            query
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        lines = []

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("202"):
                continue

            if line.startswith("main"):
                continue
            
            bad = (
                "WARN",
                "INFO",
                "package scanning",
                "Please remove",
                "logging.apache.org",
                "main "
            )

            if any(x in line for x in bad):
                continue

            lines.append(line)

        return "\n".join(lines)


    def databases(self):

        output = self._run_query("SHOW DATABASES;")

        return [
            x for x in output.splitlines()
            if x != "database_name"
        ]


    def tables(self):

        output = self._run_query(
            f"USE {self.database}; SHOW TABLES;"
        )

        return [
            x for x in output.splitlines()
            if x != "tab_name"
        ]


    def schema(self):

        output = self._run_query(
            f"USE {self.database}; DESCRIBE {self.table};"
        )

        reader = csv.reader(io.StringIO(output))

        rows = []

        for row in reader:

            if len(row) < 2:
                continue

            column = row[0].strip()
            
            if column == "col_name":
                continue            

            if not column:
                break

            if column.startswith("#"):
                break

            rows.append({
                "column": column,
                "type": row[1].strip()
            })

        return rows


    def preview(self):

        output = self._run_query(f"""
        USE {self.database};

        MSCK REPAIR TABLE customers;

        SELECT
        id,
        first_name,
        last_name,
        department,
        salary
        FROM {self.table}
        ORDER BY id ASC
        LIMIT 20;
        """)

        reader = csv.DictReader(io.StringIO(output))

        return list(reader)