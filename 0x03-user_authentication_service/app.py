#!/usr/bin/env python3
"""
App module
"""

from flask import abort, Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """Method that returns a JSON payload.

    Returns:
        string : JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """Method that registers a user.

    Returns:
        string : JSON payload
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    email = request.form.get("email")
    password = request.form.get("password")
    if Auth.valid_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    res = jsonify({"email": f"{email}", "meddage": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
