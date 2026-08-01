import subprocess
import re

from config import HDFS_CONTAINER


class HDFSService:

    def list_directory(self, path="/"):

        try:

            command = [
                "docker",
                "exec",
                HDFS_CONTAINER,
                "hdfs",
                "dfs",
                "-ls",
                path
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                return False, result.stderr

            files = []

            lines = result.stdout.splitlines()

            for line in lines:

                if line.startswith("Found"):
                    continue

                parts = re.split(r"\s+", line, maxsplit=7)

                if len(parts) < 8:
                    continue

                permissions = parts[0]
                size = parts[4]
                date = parts[5]
                time = parts[6]
                filepath = parts[7]

                name = filepath.split("/")[-1]

                files.append({
                    "name": name,
                    "path": filepath,
                    "type": (
                        "directory"
                        if permissions.startswith("d")
                        else "file"
                    ),
                    "size": size,
                    "modified": f"{date} {time}"
                })

            return True, files

        except Exception as e:

            return False, str(e)