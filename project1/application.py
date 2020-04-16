import os

from flask import Flask, session, request
from flask import Flask, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/registration", methods=["GET", "POST"])
def register():
    if(request.method == "POST"):

        name= request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email-id")

        print(name)
        print(password)
        print(email)
        return render_template("show.html", name=name)
    return render_template("registration.html")




























