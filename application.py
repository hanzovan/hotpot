from cs50 import SQL
from flask import Flask, flash, request, redirect, render_template, jsonify, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import strong_password, login_required, news
from datetime import datetime, timedelta, date


# Config app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# config SQL database
db = SQL("sqlite:///hotpot.db")


# index page
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # If user reached route by submitting form
    if request.method == "POST":
        quantity = int(request.form.get("quantity"))
        articles = news(quantity)
        return render_template("index.html", articles=articles)

    else:
        articles = news(10)
        return render_template("index.html", articles=articles)


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

        # Inform user that they register successfully and redirect them to homepage
        flash("Congratulations! You are registered!")
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

            # Inform user that they successfully logged in
            flash("You are now logged in!")
            return redirect("/")

    # If user reached route via clicking link or being redirect
    else:
        return render_template("login.html")

# Log out route
@app.route("/logout")
def logout():
    """ Allow user to log out """
    session.clear()
    flash("Logged out!")
    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    # If user reached route via submitting form
    if request.method == "POST":

        # Define variables
        username = session['username']
        password = request.form.get("password")
        new_password = request.form.get("new_password")
        new_password_confirm = request.form.get("new_password_confirm")
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check input validity:
        if not password:
            return render_template("error.html", message="Missing password")
        if not new_password:
            return render_template("error.html", message="Missing new password")
        if not new_password_confirm:
            return render_template("error.html", message="You need to confirm new password")
        if new_password != new_password_confirm:
            return render_template("error.html", message="New password doesn't match with the confirm")
        if not check_password_hash(user['hash'], password):
            return render_template("error.html", message="Incorrect password")

        # If everything is correct, change the password:
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(new_password), username)
        flash("Password changed! Congratulations!")
        return redirect("/")

    # If user reached route via clicking link
    else:
        return render_template("change_password.html")


@app.route("/add_issue", methods=["GET", "POST"])
def add_issue():

    # Check method
    if request.method == "POST":

        # Define variables:
        issue = request.form.get("issue")
        description = request.form.get("description")
        solution = request.form.get("solution")
        user = session["user_id"]

        # Check input
        if not issue:
            return render_template("error.html", message="Missing issue name")

        if not description:
            return render_template("error.html", message="Missing description")

        if not solution:
            solution = ""

        # If inputs are valid
        db.execute("INSERT INTO helpers(user_id, issue, description, solution) VALUES (?, ?, ?, ?)", user, issue, description, solution)

        return redirect("/")

    # If user reached route via clicking link or being redirect
    else:
        return render_template("add_issue.html")


@app.route("/issues", methods=["GET", "POST"])
def issues():

    # Check method
    if request.method == "POST":
        return TODO

    # If user reached route via clicking link
    else:
        issues = db.execute("SELECT * FROM helpers")

        return render_template("issues.html", issues=issues)