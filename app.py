from flask import Flask, jsonify, send_file
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("messages.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/messages")
def api_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 50")
    messages = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in messages])

@app.route("/")
def index():
    return send_file("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
