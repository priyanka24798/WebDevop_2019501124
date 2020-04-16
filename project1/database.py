from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class database(db.Model):
    __tablename__ = "Registrations"
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False,primary_key=True)
    datetime = db.Column(db.String, nullable = False)


