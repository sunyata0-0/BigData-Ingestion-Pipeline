import subprocess


class DockerService:

    # Services displayed in the dashboard
    SERVICES = {
        "Airflow": ["airflow", "airflow-db"],
        "HDFS": ["namenode", "datanode"],
        "NiFi": ["nifi"],
        "Hive": ["hive"],
        "MySQL": ["mysql"],
        "LDAP": ["ldap", "phpldapadmin"],
        "phpMyAdmin": ["phpmyadmin"]
    }

    def get_status(self):

        result = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--format",
                "{{.Names}}|{{.Status}}"
            ],
            capture_output=True,
            text=True
        )

        containers = {}

        for line in result.stdout.splitlines():

            name, status = line.split("|", 1)

            containers[name] = {
                "status": status,
                "running": status.startswith("Up")
            }

        services = []

        for service_name, members in self.SERVICES.items():

            running = True
            info = []

            for member in members:

                if member in containers:

                    info.append({
                        "name": member,
                        "status": containers[member]["status"]
                    })

                    if not containers[member]["running"]:
                        running = False

                else:

                    running = False

                    info.append({
                        "name": member,
                        "status": "Missing"
                    })

            services.append({

                "service": service_name,
                "running": running,
                "containers": info

            })

        return services

    def restart_service(self, service):

        if service not in self.SERVICES:
            return False, "Unknown service."

        containers = self.SERVICES[service]

        result = subprocess.run(
            ["docker", "restart"] + containers,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return True, f"{service} restarted successfully."

        return False, result.stderr.strip()