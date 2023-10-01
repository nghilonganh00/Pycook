from app.extensions.db import db
from app.models.ingredient_model import Ingredient
from flask import Blueprint, jsonify, request

import base64
ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/api/ingredient/create', methods = ['POST'])
def createNewIngerdient():
    data = request.json

    image_data_base64 = data.get('ingredientImage').split(",")[1]
    image_binary_data = base64.b64decode(image_data_base64)

    ingredientName = data.get('ingredientName')
    ingredientImage =  image_binary_data
    unit = data.get('unit')
    calo = data.get('calo')
    fat = data.get('fat')
    cat = data.get('cat')
    new_ingredient = Ingredient(ingredientName=ingredientName, ingredientImage=ingredientImage, unit=unit, calo=calo, fat=fat, cat=cat)
    db.session.add(new_ingredient)
    db.session.commit()

    response_data = {
        "message": "User registered successfully",
    }
    return jsonify(response_data), 201