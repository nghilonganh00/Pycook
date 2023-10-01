from app.extensions.db import db

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class FoodHashtag(db.Model):
    __tablename__ = 'FoodHashtags'

    foodhashtagId = db.Column(db.Integer, primary_key=True)
    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'))
    hashtagId = db.Column(db.Integer, db.ForeignKey('hashtags.hashtagId'))

    def __init__(self, food, hashtag):
        self.food = food
        self.hashtag = hashtag
