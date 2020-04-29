import os

from flask import Flask, session, request, url_for
from flask import redirect
from flask import Flask, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database import *
from datetime import datetime
from booksimport import *
from sqlalchemy import or_
from bookreview import *


app = Flask(__name__)
# app1 = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
# db1.init_app(app1)
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
            return render_template("registration.html", message = "Congratulation, you have successfully registered..you can now login..!")
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


        return render_template ("user.html", message= "You are Logged in as " + username)
    return redirect(url_for('register'))
   


@app.route("/auth",methods = ["GET","POST"])
def authenticate():
    # database.query.all()
    name = request.form.get("username")
    email = request.form.get("email-id")
    password = request.form.get("password")
    # member = db.session.query(database).filter_by(database.email == email).all()
    member = database.query.filter_by(email = email).first()

    if member is not None:
        if ((member.password == password and member.email == email) and member.name == name):
            session['username'] = request.form.get("email-id")
            return render_template("user.html")
        else:
            return render_template("registration.html", message = "Invalid credentials!")
    else:
        return render_template("registration.html", message = "Account does not exists..Please register!! ")


@app.route('/Search', methods=["GET","POST"])
def search():
    
    if(request.method == "POST"):
        book_search = request.form.get("search")
        
        if request.form.get("isbnsearch") == "option1":
            print(book_search +" like  "+"isbnsearch")
            s = Books.query.filter(Books.isbn.like('%'+ book_search +'%')).all()
            print(s)
            return render_template("user.html", Books = s)

        elif request.form.get("titlesearch") == "option2":
            print(book_search +" like   "+"titlesearch")
            s = db1.session.query(Books).filter((Books.tittle.like('%'+ book_search +'%')))
            print(s)
            return render_template("user.html", Books = s)
       
        elif request.form.get("authorsearch") == "option3":
            print(book_search +" like   "+"authorsearch")
            s = db1.session.query(Books).filter((Books.author.like('%'+ book_search +'%')))
            print(s)
            return render_template("user.html", Books = s)
        return render_template("user.html", message= "No books found.!")
    return render_template("user.html")


@app.route("/bookpage/<string:isbn_id>")
def book_details(isbn_id):
    book = db1.session.query(Books).filter(Books.isbn == isbn_id).all()
    review = db1.session.query(REVIEW).filter(REVIEW.isbn == isbn_id).all()
    total_reviews = db.session.query(REVIEW).filter(REVIEW.isbn == isbn_id)
    return render_template("bookpage.html", data=book, isbn_id = isbn_id, total_reviews = total_reviews)


# @app.route('/review', methods =['GET','POST'])
# def review():
#     if request.method == 'POST':
#         rating = request.form.get('review_tags')
#         review = request.form.get('review_value')
#         username = session['username']
#         t= list(request.form.items())
#         print(t)

#         if (REVIEW.query.filter_by(email = email, isbn = "1234").first() == None) :
#             data = REVIEW(email = email, isbn = "1234", rating = rating, review = review) 
#             db1.session.add(data)
#             db1.session.commit()
#         else:
#             total_reviews = db1.session.query(REVIEW).filter(REVIEW.isbn == "1234")
#             return render_template('Review.html',message = 'You have already given review',total_reviews=total_reviews,isbn = "1234")
#     total_reviews = db1.session.query(REVIEW).filter(REVIEW.isbn == "1234")
#     return render_template('Review.html', message1 = 'review submitted succesfully.',total_reviews=total_reviews,isbn = "1234")




@app.route('/review', methods =['GET','POST'])
def review():
    if request.method == 'POST':           
        rating = request.form.get('review_tags')
        review = request.form.get('review_value')
        email = session['username']
        temp = list(request.form.items())
        print(temp)
        isbn = temp[2][0]
        book = db1.session.query(Books).filter(Books.isbn == isbn).all()
        total_reviews = db.session.query(REVIEW).filter(REVIEW.isbn == isbn)
        if (REVIEW.query.filter_by(email = email, isbn = isbn).first() == None):
            data = REVIEW(email = email, isbn = isbn, rating = rating, review = review) 
            db.session.add(data)
            db.session.commit()
        else:
            return render_template('bookpage.html',message = 'You have already given review',data=book, total_reviews=total_reviews,isbn = isbn)
    return render_template('bookpage.html',email = session['username'], message1 = 'review submitted succesfully.',data=book, total_reviews=total_reviews,isbn = isbn)

@app.route("/logout")
def logout(): 
    session.pop('username', None)
    return render_template("registration.html")
