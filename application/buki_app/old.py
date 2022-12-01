from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    Response,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import hashlib, os, time
from functools import wraps
from datetime import datetime
import pytz

from flask_socketio import SocketIO, join_room
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from dotenv import load_dotenv
app = Flask(__name__, template_folder="templates")
app.config.from_object('config')
db = SQLAlchemy(app)
socketio = SocketIO(app)


def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        username = request.form["username"].strip().lower()
        password = request.form["password"]
        try:
            user = client.query(
                q.get(q.match(q.index("users_index"), username)))
            flash("User already exists with that username.")
            return redirect(url_for("login"))
        except:
            user = client.query(
                q.create(
                    q.collection("users"),
                    {
                        "data": {
                            "username":
                            username,
                            "email":
                            email,
                            "password":
                            hashlib.sha512(password.encode()).hexdigest(),
                            "date":
                            datetime.now(pytz.UTC),
                        }
                    },
                ))
            chat = client.query(
                q.create(
                    q.collection("chats"),
                    {"data": {
                        "user_id": user["ref"].id(),
                        "chat_list": [],
                    }},
                ))
            flash("Registration successful.")
            return redirect(url_for("login"))
    return render_template("auth.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        try:
            user = client.query(q.get(q.match(q.index("user_index"), email)))
            print(user)
            if (hashlib.sha512(password.encode()).hexdigest() == user["data"]
                ["password"]):
                session["user"] = {
                    "id": user["ref"].id(),
                    "username": user["data"]["username"],
                    "email": user["data"]["email"],
                }
                return redirect(url_for("chat"))
            else:
                raise Exception()
        except Exception as e:
            print(e)
            flash(
                "You have supplied invalid login credentials, please try again!"
            )
            return redirect(url_for("login"))
    return render_template("auth.html")
