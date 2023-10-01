from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.food_model import Food
from app.models.ingredient_model import Ingredient
from app.models.recipe_model import Recipe

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/api/recipe/create/', methods=["POST"])
def createRecipes():
    foodId = request.json.get('foodId')
    ingredientId = request.json.get('ingredientId')
    ingredientOrder = request.json.get('ingredientOrder')
    ingredientQuanity = request.json.get('ingredientQuanity')

    food = Food.query.get(foodId)
    ingredient = Ingredient.query.get(ingredientId)
    
   
    newRecipe = Recipe(ingredientOrder=ingredientOrder, ingredientQuanity=ingredientQuanity, food=food, ingredient=ingredient)

    try:
        db.session.add(newRecipe)
        db.session.commit()
        response_data = {
            "message": "Add successly new recipe",
        }
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        
    return jsonify(response_data), 201

