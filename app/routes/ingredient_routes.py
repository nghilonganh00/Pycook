from app.extensions.db import db
from app.models.ingredient_model import Ingredient
from flask import Blueprint, jsonify, request

import base64
ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/api/ingredient/getAll', methods=['GET'])
def getAllIngredient():
    try:
        ingredient_data = Ingredient.query.limit(20).all()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    ingredients = []
    for ingredient in ingredient_data:
        ingredient = {
            'ingredientId': ingredient.ingredientId,
            'ingredientName': ingredient.ingredientName,
            'ingredientImage': f"data:image/png;base64,{base64.b64encode(ingredient.ingredientImage).decode('utf-8') if ingredient.ingredientImage else None}",
            'unit': ingredient.unit,
            'calo': ingredient.calo,
            'fat': ingredient.fat,
            'cat': ingredient.cat
        }
        ingredients.append(ingredient)

    return jsonify(ingredients), 200

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