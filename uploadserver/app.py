from flask import Flask, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "upload"

app = Flask(__name__)

app.secret_key = "hello world"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024


@app.route('/upload', methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file in"
    file = request.files["file"]
    if file.filename == "":
        return "No file name"
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return "OK"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
