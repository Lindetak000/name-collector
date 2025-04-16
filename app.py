from flask import Flask, request, Response
from datetime import datetime
import sqlite3
import os

# Password for /names route
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "letmein")

app = Flask(__name__)

# Set up database
conn = sqlite3.connect('visitors.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS visitors (id INTEGER PRIMARY KEY, name TEXT, timestamp TEXT)')
conn.commit()

# Route to store name
@app.route("/store-name", methods=["POST"])
def store_name():
    data = request.get_json()
    name = data.get("name")
    if name:
        timestamp = datetime.utcnow().isoformat()
        c.execute("INSERT INTO visitors (name, timestamp) VALUES (?, ?)", (name, timestamp))
        conn.commit()
        return {"status": "success"}, 200
    return {"status": "no name received"}, 400

# Route to view names (password protected)
@app.route("/names", methods=["GET"])
def get_names():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return Response("Unauthorized", status=401)

    c.execute("SELECT name, timestamp FROM visitors")
    rows = c.fetchall()

    html = "<h2>Visitors:</h2><ul>"
    for name, timestamp in rows:
        html += f"<li>{name} — {timestamp}</li>"
    html += "</ul>"

    return html

# Required for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
