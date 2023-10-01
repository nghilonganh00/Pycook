from app.extensions.db import db

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipeId = db.Column(db.Integer, primary_key=True)
    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'))
    ingredientId = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientId'))
    ingredientOrder = db.Column(db.Integer, nullable=False)
    ingredientQuanity = db.Column(db.Float)
    
    def __init__(self, ingredientOrder, ingredientQuanity, food, ingredient):
        self.ingredientOrder = ingredientOrder
        self.ingredientQuanity = ingredientQuanity
        self.food = food
        self.ingredient = ingredient
