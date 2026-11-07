import mimetypes
import os
import re 
import sqlite3
from urllib.parse import quote
from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DB_PATH = os.path.join(BASE_DIR, "videos.db")
ALLOWED_EXTENSIONS = {".webm", ".mp4"}

mimetypes.add_type("video/webm", ".webm")

app = Flask(__name__)

def init_db():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL UNIQUE, 
            file_path TEXT NOT NULL,
            video_url TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    db.commit()
    db.close()

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def make_safe_name(company_name):
    return re.sub(r"[^\w-]+", "_", company_name).strip("_")

@app.route("/upload", methods=["POST"])
def upload_video():
    file = request.files.get("file")
    company_name = request.form.get("company_name", "").strip()

    if file is None or file.filename == "":
        return jsonify(error="file is required"), 400
    if not company_name:
        return jsonify(error="company_name is required"), 400

    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify(error="only .webm and .mp4 files are allowed"), 400

    safe_name = make_safe_name(company_name)
    if not safe_name:
        return jsonify(error="company_name has no valid characters"), 400

    filename = safe_name + extension
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    video_url = f"{request.host_url}media/{quote(filename)}"

    db = get_db()
    db.execute(
        """ 
        INSERT INTO videos (company_name, file_path, video_url)
        VALUES (?, ?, ?)
        ON CONFLICT(company_name) DO UPDATE SET
            file_path = excluded.file_path,
            video_url = excluded.video_url,
            updated_at = datetime('now')
        """,
        (company_name, file_path, video_url),
    )
    db.commit()

    return jsonify(company_name=company_name, video_url=video_url)

@app.route("/get_video_url", methods=["GET"])
def get_video_url():
    company_name = request.args.get("company_name", "").strip()
    if not company_name:
        return jsonify(error="company_name is required"), 400

    row = get_db().execute(
        "SELECT company_name, video_url FROM videos WHERE company_name = ?",
        (company_name,),
    ).fetchone()

    if row is None:
        return jsonify(error="company not found"), 404

    return jsonify(company_name=row["company_name"], video_url=row["video_url"])

@app.route("/media/<path:filename>", methods=["GET"])
def media(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route("/videos", methods=["GET"])
def list_videos():
    rows = get_db().execute(
        "SELECT company_name, file_path, video_url, created_at, updated_at "
        "FROM videos ORDER BY company_name"
    ).fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    init_db()
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", "8000"))
    app.run(host=host, port=port)