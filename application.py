from cs50 import SQL
from flask import Flask, flash, request, redirect, render_template, jsonify, session
from flash_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


# Config app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# config SQL database
db = SQL("sqlite:///hotpot.db")


# index page
@app.route("/")
def index():
    return render_template("index.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # If user reached route via submitting form:
    if request.method == "POST":
        # Define variable:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if not username:
            return render_template("error.html", message="Missing username")
        if not

    # If user reached route via clicking link or being redirect
    else:
        return render_template("login.html")