#!/usr/bin/env python3
"""flask app """

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    response = jsonify({"message": "Bienvenue"})
    return response


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """post  a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /session
    respond with a 401 HTTP status or
    {"email": "<user email>", "message": "logged in"}
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        res = jsonify({"email": f"{email}", "message": "logged in"})
        res.set_cookie("session_id", AUTH.create_session(email))
        return res
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
