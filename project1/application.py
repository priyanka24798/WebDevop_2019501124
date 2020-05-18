import os

from flask import Flask, session, request, url_for
from flask import redirect
from flask import jsonify, json
from flask import Flask, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database import *
from datetime import datetime
from booksimport import *
from sqlalchemy import or_
from review import *
import requests


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


@app.route('/api/search/<search>')
def api_search(search):
    searchbook = search
    result =  Books.query.filter(or_((Books.isbn.like('%'+ searchbook +'%')),(Books.tittle.like('%'+ searchbook +'%') ),(Books.author.like('%'+ searchbook +'%')))).all()
    if (len(result)== 0) :
        return jsonify ({"ERROR": "BOOK NOT FOUND"}), 400
    
    booktitle =[]
    bookisbn = []
    bookauthor=[]
    for i in result:
        booktitle.append(i.tittle)
        bookauthor.append(i.author)
        bookisbn.append(i.isbn)
    
    return jsonify({
        "ISBN" : bookisbn,
        "AUTHOR": bookauthor,
        "TITLE": booktitle,
    })

@app.route("/api/review",methods = ["POST"])
def apibookpagereview():
   isbn = request.form.get("isbn")
   total_reviews = db1.session.query(REVIEW).filter(REVIEW.isbn == isbn)
   
#    print(len(list(total_reviews)))
   tot_reviews = {}
   for i in total_reviews:
       tot_reviews[i.username] = [i.review,i.rating] 
   print(tot_reviews)
   return jsonify({'total_review': tot_reviews})

@app.route("/api/submit-review", methods = ["POST"])
def submitReview():
    rating = request.form.get('rating')
    review = request.form.get('review')
    isbn = request.form.get('isbn')
    email = session['username']
    # print(name)
    r = REVIEW.query.filter_by(email = email, isbn = isbn).first()
    # flag = review_present(name,isbn)
    # print(r)
    if r is None:
        data = REVIEW(email = email, isbn = isbn, rating = rating, review = review)
        db.session.add(data)
        db.session.commit()
        # return jsonify({'flag1': 'true'})
        return jsonify({"email" : [True,email]})
    return jsonify({"email": [False, email]})




@app.route("/bookpage/<string:isbn_id>")
def book_details(isbn_id):
    book = db1.session.query(Books).filter(Books.isbn == isbn_id).all()
    review = db1.session.query(REVIEW).filter(REVIEW.isbn == isbn_id).all()
    total_reviews = db.session.query(REVIEW).filter(REVIEW.isbn == isbn_id)
    return render_template("bookpage.html", data=book, isbn_id = isbn_id, total_reviews = total_reviews)




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

    
