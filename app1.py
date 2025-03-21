from flask import Flask, jsonify, send_file
from telethon import TelegramClient, events
import sqlite3
import os
import json

# Thông tin API Telegram cá nhân
API_ID = 22285674  # Thay bằng API ID của bạn
API_HASH = "be6f483db023e566f85aba51181f3582"  # Thay bằng API Hash của bạn
SESSION_NAME = "my_session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

app = Flask(__name__)

# Kết nối SQLite
def get_db_connection():
    conn = sqlite3.connect("messages.db")
    conn.row_factory = sqlite3.Row
    return conn

# API: Lấy tin nhắn từ database và gửi JSON về frontend
@app.route("/api/messages")
def api_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 50")
    messages = cursor.fetchall()
    conn.close()
    
    return app.response_class(
        response=json.dumps([dict(row) for row in messages], ensure_ascii=False),
        status=200,
        mimetype="application/json"
    )

# Khi có tin nhắn mới, lưu thêm tên và username của người gửi
@client.on(events.NewMessage)
async def handle_message(event):
    sender = await event.get_sender()
    
    user_id = sender.id
    first_name = sender.first_name if sender.first_name else "Unknown"
    username = sender.username if sender.username else "NoUsername"
    user_message = event.message.text

    # Kết nối database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra và tạo bảng nếu chưa có
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            first_name TEXT,
            username TEXT,
            user_message TEXT,
            bot_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Lưu tin nhắn vào database
    cursor.execute("""
        INSERT INTO messages (user_id, first_name, username, user_message, bot_response)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, first_name, username, user_message, ""))

    conn.commit()
    conn.close()

# Flask route chính
@app.route("/")
def index():
    return "Userbot Telegram đang chạy!"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    with client:
        client.start()
        from threading import Thread
        Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
        client.run_until_disconnected()
