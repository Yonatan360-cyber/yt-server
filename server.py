from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import zipfile
import tempfile

app = Flask(__name__)
CORS(app)  # מאפשר בקשות מכל מקור

DOWNLOAD_FOLDER = tempfile.gettempdir()  # תקייה זמנית

@app.route("/download", methods=["GET"])
def download_channel():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    # תקייה זמנית ל־yt-dlp
    temp_dir = tempfile.mkdtemp(dir=DOWNLOAD_FOLDER)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
    }

    # תחילת הורדה – מחזיר מיד
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # יצירת ZIP
    zip_path = os.path.join(DOWNLOAD_FOLDER, "channel.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    return send_file(zip_path, as_attachment=True, download_name="channel.zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
