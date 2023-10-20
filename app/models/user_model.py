from app.extensions.db import db

from app.models.follower_model import Follower
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    pycookID = db.Column(db.String(25), unique=True)
    fullname = db.Column(db.String(45), nullable=False)
    avatar = db.Column(db.BLOB)

    followers = db.relationship('Follower', foreign_keys=[Follower.followerId], backref='follower')
    followedBy =db. relationship('Follower', foreign_keys=[Follower.followedId], backref='followed')
    favourite_foods = db.relationship('FavoriteFood', back_populates='user')
    foods = db.relationship("Food", backref="user", lazy=True)
    comments = db.relationship("Comment", back_populates="user")

    def __init__(self, username, password, pycookID, fullname, avatar):
        self.username = username
        self.password = password
        self.pycookID = pycookID
        self.fullname = fullname
        self.avatar = avatar
