from flask import Flask, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('visitors.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS visitors (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

@app.route("/store-name", methods=["POST"])
def store_name():
    data = request.get_json()
    name = data.get("name")
    if name:
        c.execute("INSERT INTO visitors (name) VALUES (?)", (name,))
        conn.commit()
        return {"status": "success"}, 200
    return {"status": "no name received"}, 400

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or default to 5000
    app.run(host='0.0.0.0', port=port)
