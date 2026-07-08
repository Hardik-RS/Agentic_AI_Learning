from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Store conversation history
chat_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Add user message to history
    chat_history.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": chat_history,
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    result = response.json()

    assistant_reply = result["choices"][0]["message"]["content"]

    # Save assistant response
    chat_history.append({
        "role": "assistant",
        "content": assistant_reply
    })

    return jsonify({
        "response": assistant_reply,
        #"history": chat_history
    })


@app.route("/history", methods=["GET"])
def history():
    return jsonify(chat_history)


@app.route("/clear", methods=["POST"])
def clear():
    global chat_history

    chat_history = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    return jsonify({"message": "History cleared"})


if __name__ == "__main__":
    app.run(debug=True)