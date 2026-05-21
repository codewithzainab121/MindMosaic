from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ai_agent import get_ai_response
from crisis import detect_crisis, detect_stress, get_crisis_response
import json, os, uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ====================== PATH SETUP ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_FOLDER = os.path.join(BASE_DIR, 'frontend')
SESSIONS_FILE = os.path.join(BASE_DIR, "sessions.json")

# ====================== FRONTEND ROUTES ======================
@app.route('/')
def home():
    return jsonify({"status": "MindMosaic backend is running 🚀"})

@app.route('/style.css')
def serve_css():
    return send_from_directory(FRONTEND_FOLDER, 'style.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory(FRONTEND_FOLDER, 'script.js')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# ====================== HELPERS ======================
def load_sessions():
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_sessions(data):
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ====================== API ======================
@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json()
    session_id = body.get("session_id") or str(uuid.uuid4())
    user_msg = body.get("message", "").strip()

    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    sessions = load_sessions()

    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "created_at": datetime.now().isoformat()
        }

    history = sessions[session_id]["history"]

    # Crisis logic
    if detect_crisis(user_msg):
        reply = get_crisis_response()
        msg_type = "crisis"
    else:
        reply = get_ai_response(history, user_msg)
        msg_type = "stress" if detect_stress(user_msg) else "normal"

    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": reply})

    sessions[session_id]["history"] = history
    save_sessions(sessions)

    return jsonify({
        "session_id": session_id,
        "reply": reply,
        "type": msg_type
    })

@app.route("/api/history/<session_id>", methods=["GET"])
def get_history(session_id):
    sessions = load_sessions()
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(sessions[session_id])

@app.route("/api/new-session", methods=["POST"])
def new_session():
    sid = str(uuid.uuid4())
    sessions = load_sessions()
    sessions[sid] = {"history": [], "created_at": datetime.now().isoformat()}
    save_sessions(sessions)
    return jsonify({"session_id": sid})

@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    sessions = load_sessions()
    result = []

    for sid, data in sessions.items():
        h = data.get("history", [])
        first = next((m["content"][:40] for m in h if m["role"] == "user"), "New Session")

        result.append({
            "id": sid,
            "preview": first,
            "created_at": data.get("created_at", "")
        })

    result.sort(key=lambda x: x["created_at"], reverse=True)
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ====================== RAILWAY FIX (IMPORTANT) ======================
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )