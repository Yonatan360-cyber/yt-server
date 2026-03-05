from flask import Flask, request, jsonify
import yt_dlp
import os
import threading

app = Flask(__name__)

# תיקייה לשמירת ההורדות
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "yt_dl")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_channel(url):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(channel)s - %(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
        'embedthumbnail': True,
        'embedmetadata': True,
        'noplaylist': False,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # הרצה ב-thread כדי שהשרת לא יחסום
    threading.Thread(target=download_channel, args=(url,), daemon=True).start()
    return jsonify({"status": "started", "message": f"Downloading {url} in background"}), 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render מספק PORT
    app.run(host="0.0.0.0", port=port)
