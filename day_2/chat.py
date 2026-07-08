from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests
import os
import uuid

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------
# Hugging Face API
# -------------------------------------------------
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# -------------------------------------------------
# Database Model
# -------------------------------------------------
class Messages(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# -------------------------------------------------
# Session ID
# -------------------------------------------------
SESSION_ID = "96e936b6-f4a2-49c8-9e0e-50620c79012e"

# -------------------------------------------------
# Routes
# -------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # -----------------------------
    # Save user message
    # -----------------------------
    db.session.add(
        Messages(
            session_id=SESSION_ID,
            role="user",
            content=user_message
        )
    )

    db.session.commit()

    # -----------------------------
    # Load history
    # -----------------------------
    db_messages = (
        Messages.query
        .filter_by(session_id=SESSION_ID)
        .order_by(Messages.id)
        .all()
    )

    history = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    for msg in db_messages:
        history.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    # -----------------------------
    # Send to LLM
    # -----------------------------
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": history,
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        return jsonify(
            {"error": response.text}
        ), response.status_code

    result = response.json()

    assistant_reply = result["choices"][0]["message"]["content"]

    # -----------------------------
    # Save assistant reply
    # -----------------------------
    db.session.add(
        Messages(
            session_id=SESSION_ID,
            role="assistant",
            content=assistant_reply
        )
    )

    db.session.commit()

    return jsonify({
        "response": assistant_reply,
        "session_id": SESSION_ID
    })


@app.route("/history", methods=["GET"])
def history():

    db_messages = (
        Messages.query
        .filter_by(session_id=SESSION_ID)
        .order_by(Messages.id)
        .all()
    )

    history = []

    for msg in db_messages:
        history.append(
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": str(msg.created_at)
            }
        )

    return jsonify(history)


@app.route("/clear", methods=["POST"])
def clear():

    Messages.query.filter_by(
        session_id=SESSION_ID
    ).delete()

    db.session.commit()

    return jsonify(
        {
            "message": "History cleared"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
