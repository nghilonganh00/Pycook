from app.extensions.db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Follower(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)
    followedId = db.Column(db.Integer, db.ForeignKey("users.id"))
    followerId = db.Column(db.Integer, db.ForeignKey("users.id"))
