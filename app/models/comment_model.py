from app.extensions.db import db

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    commentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'))
    commentContent = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user, food, commentContent):
        self.user = user
        self.food = food
        self.commentContent = commentContent
