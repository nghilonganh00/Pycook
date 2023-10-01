from app.extensions.db import db

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    ingredientId = db.Column(db.Integer, primary_key=True)
    ingredientName = db.Column(db.String(80), unique=False, nullable=False)
    ingredientImage = db.Column(db.BLOB, nullable = True)
    unit = db.Column(db.String(80), unique=False, nullable=False)
    calo = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    cat = db.Column(db.Integer, nullable=False)

    def __init__(self, ingredientName, ingredientImage, unit, calo, fat, cat):
        self.ingredientName = ingredientName
        self.ingredientImage = ingredientImage
        self.unit = unit
        self.calo = calo
        self.fat = fat
        self.cat = cat
