from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import random
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS (Netlify support)
CORS(app)

# Rate limiting (anti abuse)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

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
        "service": "ZIP Unlocker Simulator API",
        "version": "1.0",
        "note": "This is a simulation backend"
    })


@app.route("/unlock", methods=["POST"])
@limiter.limit("5 per minute")
def unlock():
    if not request.is_json:
        return error("JSON body required")

    data = request.get_json()

    filename = data.get("filename")
    wordlist_size = data.get("wordlist_size", 1000)

    # Validation
    if not filename:
        return error("filename is required")

    if not isinstance(wordlist_size, int) or wordlist_size <= 0:
        return error("wordlist_size must be a positive number")

    # Simulate processing
    time.sleep(2)

    found = random.choice([True, False])

    result = {
        "file": filename,
        "checked_passwords": wordlist_size,
        "password_found": found,
        "password": "demo123" if found else None,
        "engine": "SIMULATOR",
        "legal": True
    }

    return success(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# ❌ Production me app.run nahi likhte