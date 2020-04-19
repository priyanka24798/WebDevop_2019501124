import os

from flask import Flask, session, request, url_for
from flask import redirect
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

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key= "log-in"



@app.route("/registration", methods=["GET", "POST"])
def register():
    if(request.method == "POST"):
        database.query.all()
        name= request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email-id")
        register = database(name= name,email=email,password = password, datetime = datetime.now())
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

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return 'You are Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"
   


@app.route("/auth",methods = ["GET","POST"])
def authenticate():
    database.query.all()
    name = request.form.get("username")
    email = request.form.get("email-id")
    log = database(name =  name ,email = email)
    try:
        Member = db.session.query(database).filter(database.email == email).all()
        print(Member[0].name)
        session['username'] = request.form.get("email-id")
        # return render_template("user.html",f= name,email = email)  
        return redirect(url_for('index'))
    except Exception:
        return render_template("error.html")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("registration.html")