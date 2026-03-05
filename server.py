from flask import Flask, request, send_file
import subprocess
import uuid
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "/tmp/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    filename = os.path.join(DOWNLOAD_FOLDER, f"{uuid.uuid4()}.mp3")

    try:
        subprocess.run([
            "yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3",
            "-o", filename, url
        ], check=True)
    except Exception as e:
        return f"Download failed: {str(e)}", 500

    resp = send_file(filename, as_attachment=True)
    os.remove(filename)
    return resp

@app.route("/")
def home():
    return "Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
