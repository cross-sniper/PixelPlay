from flask import Flask, send_from_directory, render_template_string
import os
import json

app = Flask(__name__)

# Ensure the media directory exists
MEDIA_DIR = "media"
if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

@app.route("/")
def index():
    try:
        file_list = os.listdir(MEDIA_DIR)
    except FileNotFoundError:
        return "Media directory not found.", 404
    
    files = []
    formats = [".webm", ".gif", ".mp4"]
    for file in file_list:
        if any(file.endswith(format) for format in formats):
            files.append(file)
    
    with open("web/index.html") as f:
        content = f.read()
    
    return render_template_string(content.replace("$$", json.dumps(files)))

@app.route("/media/<path:filename>")
def media(filename):
    # Sanitize file path to prevent directory traversal attacks
    safe_path = os.path.normpath(filename)
    if safe_path.startswith(".."):
        return "Invalid file path.", 400
    return send_from_directory(MEDIA_DIR, filename)

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
