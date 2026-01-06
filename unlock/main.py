from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import random
import os
import uuid

app = Flask(__name__)
CORS(app)

# Rate limit
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

# Temp upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# Helpers
# -------------------------
def error(msg, code=400):
    return jsonify({
        "status": "error",
        "message": msg
    }), code


def success(data):
    return jsonify({
        "status": "success",
        "data": data
    })


# -------------------------
# Routes
# -------------------------

@app.route("/", methods=["GET"])
def home():
    return success({
        "service": "Archive Recovery Tool API",
        "mode": "SIMULATION",
        "legal": True
    })


@app.route("/unlock", methods=["POST"])
@limiter.limit("5 per minute")
def unlock():
    # Files check
    if "zipfile" not in request.files or "wordlist" not in request.files:
        return error("zipfile and wordlist files are required")

    zip_file = request.files["zipfile"]
    wordlist_file = request.files["wordlist"]

    if zip_file.filename == "" or wordlist_file.filename == "":
        return error("Invalid file selection")

    # Save files temporarily (NO processing)
    job_id = str(uuid.uuid4())[:8]

    zip_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{zip_file.filename}")
    wordlist_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{wordlist_file.filename}")

    zip_file.save(zip_path)
    wordlist_file.save(wordlist_path)

    # ⚠️ SAFE SIMULATION (no cracking)
    time.sleep(2)

    found = random.choice([True, False])

    result = {
        "job_id": job_id,
        "archive": zip_file.filename,
        "wordlist": wordlist_file.filename,
        "password_found": found,
        "password": "demo123" if found else None,
        "engine": "SIMULATOR",
        "note": "No real cracking performed"
    }

    return success(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ❌ app.run() mat likhna (Render / Gunicorn use karega)
