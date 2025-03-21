from flask import Flask, jsonify, send_file
import sqlite3
import os

app = Flask(__name__)

# Hàm kết nối đến SQLite
def get_db_connection():
    conn = sqlite3.connect("messages.db")  # Tạo file database SQLite
    conn.row_factory = sqlite3.Row
    return conn

# API lấy tin nhắn
@app.route("/api/messages")
def api_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tạo bảng nếu chưa có
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Lấy 50 tin nhắn gần nhất
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 50")
    messages = cursor.fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in messages])

# Giao diện chính
@app.route("/")
def index():
    return send_file("index.html")

# Chạy Flask trên Render
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render sẽ
