from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Hardcoded Credentials - Vulnerable
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Create database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Welcome to the insecure app!"

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ❌ SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful!"
    else:
        return "Login failed."

if __name__ == "__main__":
    init_db()
    app.run(debug=True)