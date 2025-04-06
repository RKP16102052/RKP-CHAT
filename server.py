from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

HISTORY_FILE = "/data/history.json"

# Убедимся, что папка /data существует (для локального запуска)
os.makedirs("/data", exist_ok=True)

# Загружаем историю
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

history = load_history()

def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)

@app.route('/message', methods=['POST'])
def add_message():
    data = request.get_json()
    message = data.get("text")  # теперь клиент должен отправлять { "text": "..." }
    if message:
        history.append(message)
        save_history()
        return jsonify({"status": "ok"})
    return jsonify({"error": "No message received"}), 400

@app.route('/clear', methods=['POST'])
def clear_history():
    history.clear()
    save_history()
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
