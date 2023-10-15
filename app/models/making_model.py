from app.extensions.db import db

from sqlalchemy.orm import relationship, sessionmaker

class Making(db.Model):
    __tablename__ = 'makings'

    foodId = db.Column(db.Integer, db.ForeignKey('foods.foodId'), primary_key=True)
    makingOrder = db.Column(db.Integer, primary_key=True)
    makingContent = db.Column(db.String(255), nullable=False)
    makingImage = db.Column(db.String(255), nullable=True)

    food = relationship('Food', back_populates='makings')
    def __init__(self, food, makingOrder, makingContent, makingImage):
        self.food = food
        self.makingOrder = makingOrder
        self.makingContent = makingContent
        self.makingImage = makingImage
