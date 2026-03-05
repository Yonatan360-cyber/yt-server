from flask import Flask, request, send_file
import subprocess
import io

app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    mp3_data = io.BytesIO()

    # yt-dlp שולח את הפלט ל־stdout
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "-x",
        "--audio-format", "mp3",
        "-o", "-",  # שים "-" כדי לפלט ל-stdout
        url
    ]

    # הפלט של yt-dlp יישמר ב-mp3_data
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        mp3_data.write(process.stdout)
        mp3_data.seek(0)
    except Exception as e:
        return f"Error: {str(e)}", 500

    return send_file(mp3_data, download_name="channel.mp3", mimetype="audio/mpeg")

@app.route("/")
def home():
    return "Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
