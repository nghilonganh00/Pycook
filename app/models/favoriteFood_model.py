from app.extensions.db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class FavoriteFood(db.Model):
    __tablename__ = "favoriteFoods"


    userId = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'), primary_key=True)

    user = relationship('User', back_populates='favourite_foods')
    food = relationship('Food', back_populates='favourite_foods')

    def __init__(self, user, food):
        self.user = user
        self.food = food
