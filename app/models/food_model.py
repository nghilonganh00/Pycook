from app.extensions.db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class Food(db.Model):
    __tablename__ = "foods"

    foodId = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    foodImage = db.Column(db.String(400), nullable=False)
    foodName = db.Column(db.String(80), unique=False, nullable=False)
    foodNation = db.Column(db.String(80), unique=False, nullable=False)
    foodTime = db.Column(db.Integer, unique=False, nullable=False)
    recipes = db.Column(db.String(255), unique=False, nullable=False)
    foodDescription = db.Column(db.Text, unique=False, nullable=False)
    servingFor = db.Column(db.Integer, unique=False, nullable=False)
    deliciousTotal = db.Column(db.Integer, nullable=False, server_default="0")
    heartTotal = db.Column(db.Integer, nullable=False, server_default="0")
    likeTotal = db.Column(db.Integer, nullable=False, server_default="0")
    viewTotal = db.Column(db.Integer, nullable=False, server_default="0")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = relationship("Comment", back_populates="food")
    makings = relationship("Making", back_populates="food")

    def __init__(
        self,
        foodName,
        foodImage,
        foodNation,
        foodTime,
        recipes,
        foodDescription,
        servingFor,
        user,
    ):
        self.foodName = foodName
        self.foodImage = foodImage
        self.foodNation = foodNation
        self.foodTime = foodTime
        self.recipes = recipes
        self.foodDescription = foodDescription
        self.servingFor = servingFor
        self.deliciousTotal = 0
        self.heartTotal = 0
        self.likeTotal = 0
        self.viewTotal = 0
        self.user = user
