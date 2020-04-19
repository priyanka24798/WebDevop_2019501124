from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class database(db.Model):
    __tablename__ = "USERS"
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False,primary_key=True)
    password = db.Column(db.String, nullable = False)
    datetime = db.Column(db.String, nullable = False)


