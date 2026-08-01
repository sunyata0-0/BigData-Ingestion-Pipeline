import os
from werkzeug.utils import secure_filename


class UploadService:

    ALLOWED_EXTENSIONS = {
        "csv",
        "json",
        "xml",
        "txt",
        "dat",
        "log"
    }

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

        os.makedirs(self.upload_folder, exist_ok=True)


    def allowed_file(self, filename):

        if "." not in filename:
            return False

        extension = filename.rsplit(".", 1)[1].lower()

        return extension in self.ALLOWED_EXTENSIONS


    def save(self, file):

        if file.filename == "":
            return False, "No file selected."

        if not self.allowed_file(file.filename):
            return False, "Unsupported file type."

        filename = secure_filename(file.filename)

        destination = os.path.join(
            self.upload_folder,
            filename
        )

        file.save(destination)

        return True, f"{filename} uploaded successfully."