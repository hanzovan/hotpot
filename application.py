from cs50 import SQL
from flask import Flask, flash, request, redirect, render_template, jsonify, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import strong_password
from datetime import datetime, timedelta, date


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


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    # If user reached route via submitting form:
    if request.method == "POST":
        # Define variable:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        today = str(date.today())

        # Check user inputs
        if not username:
            return render_template("error.html", message="Missing username")
        if not password:
            return render_template("error.html", message="Missing password")
        if not password_confirm:
            return render_template("error.html", message="You need to confirm your password")
        if password != password_confirm:
            return render_template("error.html", message="Passwords don't match")
        if not strong_password(password):
            return render_template("error.html", message="Your password is not strong enought")

        # Check database
        check = db.execute("SELECT * FROM users WHERE username = ?", username)

        if check:
            return render_template("error.html", message="Username is already existed")
        else:
            db.execute("INSERT INTO users(username, hash, created) VALUES(?, ?, ?)",
                    username, generate_password_hash(password), today)

        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        session['user_id'] = user[0]['id']
        session['username'] = user[0]['username']
        return redirect("/")

    # If user reached route via clicking link or being redirect
    else:
        return render_template("register.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    # If user reach route via submitting form
    if request.method == "POST":

        # Define variables:
        username = request.form.get("username")
        password = request.form.get("password")

        # Check user input
        if not username:
            return render_template("error.html", message="Missing username")
        if not password:
            return render_template("error.html", message="Missing password")

        # Check database:
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not user or not check_password_hash(user[0]['hash'], password):
            return render_template("error.html", message="username or password incorrect")
        else:
            session['user_id'] = user[0]['id']
            session['username'] = username
            return redirect("/")

    # If user reached route via clicking link or being redirect
    else:
        return render_template("login.html")

# Log out route
@app.route("/logout")
def logout():
    """ Allow user to log out """
    session.clear()
    return redirect("/")