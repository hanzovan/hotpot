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