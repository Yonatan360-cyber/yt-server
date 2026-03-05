from flask import Flask, request, send_file
import subprocess
import uuid

app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")
    filename = f"{uuid.uuid4()}.mp3"

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "-x", "--audio-format", "mp3",
        "-o", filename,
        url
    ]

    subprocess.run(command)

    return send_file(filename, as_attachment=True)

@app.route("/")
def home():
    return "Server Running"

app.run(host="0.0.0.0", port=10000)
