import os
from functools import wraps

from flask import Flask, session, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "123"
socketio = SocketIO(app)


logged_in_users = []


def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check that user is logged in
        if "username" in session:
            return func(*args, **kwargs)
        return "Your are not authorized"

    return wrapper


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("chat"))
    return render_template("index.html", page_title="Login")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")

    # check that username is not empty
    if not username:
        return "Username is empty"

    # check that username is free
    if username in logged_in_users:
        return "Username is busy"

    # create session for new user
    session["username"] = username
    print(session)
    logged_in_users.append(username)

    return redirect(url_for("chat"))


@app.route("/chat")
@logged_in
def chat():
    return render_template(
        "chat.html", page_title="Chat", username=session.get("username")
    )


if __name__ == "__main__":
    socketio.run(app)
