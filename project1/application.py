import os

from flask import Flask, session, request
from flask import Flask, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database import *
from datetime import datetime

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return "Project 1: TODO"



@app.route("/registration", methods=["GET", "POST"])
def register():
    if(request.method == "POST"):
        database.query.all()
        name= request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email-id")
        register = database(name= name,email=email,datetime = datetime.now())
        try:
            db.session.add(register)
            db.session.commit()
            print(name)
            print(password)
            print(email)
            return render_template("show.html", name=name)
        except Exception:
            return render_template("error.html")
    return render_template("registration.html")

@app.route("/admin")
def users():
    r = database.query.all()
    return render_template("admin.html",register= r)      


@app.route("/auth",methods = ["GET","POST"])
def authenticate():
    database.query.all()
    name = request.form.get("username")
    email = request.form.get("email-id")
    log = database(name =  name ,email = email)
    try:
        Member = db.session.query(database).filter(database.email == email).all()
        print(Member[0].name)
        return render_template("user.html",f= name,email = email)  
    except Exception:
        return render_template("error.html")