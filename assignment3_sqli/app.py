import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

from database import DB_PATH


app = Flask(__name__)


def vulnerable_login(username: str, password: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    connection.close()

    return user, query


def secure_login(username: str, password: str):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    connection.close()

    return user, query


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    executed_query = None
    login_type = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        login_type = request.form.get("login_type", "")

        if login_type == "vulnerable":
            user, executed_query = vulnerable_login(username, password)
        else:
            user, executed_query = secure_login(username, password)

        result = "Login successful" if user else "Login failed"

    return render_template(
        "index.html",
        result=result,
        executed_query=executed_query,
        login_type=login_type,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
