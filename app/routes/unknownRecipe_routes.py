from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.unknownRecipe_model import unknownRecipe
from app.models.food_model import Food

unknownRecipe_bp = Blueprint('unknownRecipe_bp', __name__)

@unknownRecipe_bp.route('/api/unr/getAll/', methods=["GET"])
def get_unknownRecipes():
    unknownRecipes = unknownRecipe.query.all()
    unknownRecipe_list = [{'id': unknownRecipe.id, 'unknownRecipeName': unknownRecipe.unknownRecipeName} for unknownRecipe in unknownRecipes]
    return jsonify(unknownRecipe_list)

@unknownRecipe_bp.route('/api/unr/create/', methods=["POST"])
def create_unknownRecipes():
    unknownRecipes_data = request.json.get('unknownRecipes')

    foodId = request.json.get('foodId')
    food = Food.query.get(foodId)
    for unknownRecipe_data in unknownRecipes_data:
        un_ingredientName = unknownRecipe_data['un_ingredientName']
        un_ingredientQuanity = unknownRecipe_data['un_ingredientQuanity']
        un_ingredientUnit = unknownRecipe_data['un_ingredientUnit']
        un_ingredientOrder = unknownRecipe_data['un_ingredientOrder']

        
        new_unknownRecipe = unknownRecipe(un_ingredientName=un_ingredientName, un_ingredientQuanity=un_ingredientQuanity, un_ingredientUnit=un_ingredientUnit, un_ingredientOrder=un_ingredientOrder, food=food)
        try:
            db.session.add(new_unknownRecipe)
            db.session.commit()
            response_data = {
                "message": "User registered successfully",
            }
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    return jsonify(response_data), 201
