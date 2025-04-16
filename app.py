from flask import Flask, request, Response
from datetime import datetime
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Password for viewing /names
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "letmein")

app = Flask(__name__)

# Set up the SQLite database
conn = sqlite3.connect('visitors.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS visitors (id INTEGER PRIMARY KEY, name TEXT, timestamp TEXT)')
conn.commit()

# Route to store a name
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

# Route to view names (protected with password)
@app.route("/names", methods=["GET"])
def get_names():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return Response("Unauthorized", status=401)

    c.execute("SELECT name, timestamp FROM visitors")
    rows = c.fetchall()

    html = """
    <html>
    <head>
        <title>Visitors</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f4f8;
                padding: 2rem;
                color: #333;
            }
            h2 {
                color: #222;
                margin-bottom: 1rem;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background: white;
                margin-bottom: 1rem;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            }
            small {
                color: #777;
            }
        </style>
    </head>
    <body>
        <h2>Visitor Log</h2>
        <ul>
    """

    for name, timestamp in rows:
        html += f"<li><strong>{name}</strong><br><small>{timestamp}</small></li>"

    html += """
        </ul>
    </body>
    </html>
    """

    return html

# Run the app (used by Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
