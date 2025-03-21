from flask import Flask, jsonify, send_file
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="okbabe_customers",
    password="ckiuvk12",
    database="okbabe_customers",
    charset="utf8mb4"
)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/messages")
def api_messages():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT user_id, user_message, bot_response, created_at
        FROM messages
        ORDER BY created_at DESC
        LIMIT 50
    """)
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
