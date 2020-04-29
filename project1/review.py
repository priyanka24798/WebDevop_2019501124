import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
db1 = SQLAlchemy()

class REVIEW(db1.Model):
    __tablename__= "REVIEW"
    email = db1.Column(db1.String, nullable = False,primary_key=True)
    isbn = db1.Column(db1.String, nullable = False,primary_key=True)
    rating = db1.Column(db1.Integer,nullable = False)
    review = db1.Column(db1.String,nullable = False)

    def __init__(self,email,isbn,rating,review):
        self.email=email
        self.isbn=isbn
        self.rating=rating
        self.review=review

db1.init_app(app)


def main():
    # Create tables based on each table definition in `models`
    db1.create_all()

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()