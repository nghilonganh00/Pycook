from app.extensions.db import db
from sqlalchemy.orm import relationship

class unknownRecipe(db.Model):
    __tablename__ = 'unknownRecipes'

    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'), primary_key=True)
    food = relationship('Food', back_populates='unknownRecipes')
    un_ingredientName = db.Column(db.String(80), nullable=False)
    un_ingredientQuanity = db.Column(db.Float)
    un_ingredientUnit = db.Column(db.String(45))
    un_ingredientOrder = db.Column(db.Integer, primary_key=True)


    def __init__(self, un_ingredientName, un_ingredientQuanity, un_ingredientUnit, un_ingredientOrder, food):
        self.un_ingredientName = un_ingredientName
        self.un_ingredientQuanity = un_ingredientQuanity
        self.un_ingredientUnit = un_ingredientUnit
        self.un_ingredientOrder = un_ingredientOrder
        self.food = food
    
