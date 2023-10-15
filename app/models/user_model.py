from app.extensions.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    pycookID = db.Column(db.String(25), unique=True)
    fullname = db.Column(db.String(45), nullable=False)
    avatar = db.Column(db.BLOB)
    foods = db.relationship('Food', backref='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user')
    def __init__(self, username, password, pycookID, fullname, avatar):
        self.username = username
        self.password = password
        self.pycookID = pycookID
        self.fullname = fullname
        self.avatar = avatar
  
