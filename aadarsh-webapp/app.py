from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "users.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        return redirect(url_for("index"))

    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return render_template("index.html", users=users)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        conn.execute(
            "UPDATE users SET name=?, email=? WHERE id=?",
            (name, email, id)
        )
        conn.commit()
        return redirect(url_for("index"))

    user = conn.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run()
