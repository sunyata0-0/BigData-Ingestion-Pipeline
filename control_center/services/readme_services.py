from pathlib import Path


class ReadmeService:

    def load(self):

        path = Path("README.md")

        if not path.exists():
            raise FileNotFoundError("README.md not found.")

        return path.read_text(encoding="utf-8")