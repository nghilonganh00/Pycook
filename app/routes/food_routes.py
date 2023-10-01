from app.extensions.db import db
from flask import Blueprint, jsonify, request
import base64

from app.models.food_model import Food
from app.models.user_model import User

food_bp = Blueprint('food_bp', __name__)


@food_bp.route('/api/food/getByFoodId', methods=["GET"])
def getFoodByFoodId():
    foodId = request.args.get("foodId")
    food = Food.query.get(foodId)

    if food:
        chef = {
            'userId': food.user.id,
            'username': food.user.username,
            'emmai': food.user.email
        }

        unknownRecipe = []

        for ingredient in food.unknownRecipes:
            unknownRecipe.append({
                "unrOrder": ingredient.un_ingredientOrder,
                "unrName": ingredient.un_ingredientName,
                "unrQuanity": ingredient.un_ingredientQuanity,
                "unrUnit": ingredient.un_ingredientUnit
            })

        result = {
            'foodId': food.foodId,
            'chef': chef,
            'foodName': food.foodName,
            'foodImage': base64.b64encode(food.foodImage).decode('utf-8') if food.foodImage else None,
            'unknownRecipe': unknownRecipe,
            'foodNation': food.foodNation,
            'foodTime': food.foodTime,
            'foodDescription': food.foodDescription,
            'servingFor': food.servingFor,
            'deliciousTotal': food.deliciousTotal,
            'heartTotal': food.heartTotal,
            'likeTotal': food.likeTotal,
            'created_at': food.created_at
        }
        food.viewTotal += 1
        db.session.commit()
        return jsonify(result), 200
    else:
        return jsonify('Khong tim thay food'), 404
    
@food_bp.route('/api/food/create', methods=["POST"])
def create_food():
    userId = request.json.get('userId')
    foodName = request.json.get('foodName')
    foodNation = request.json.get('foodNation')
    foodTime = request.json.get('foodTime')
    foodDescription = request.json.get('foodDescription')
    servingFor = request.json.get('servingFor')

    foodImage = request.json.get('foodImage').split(",")[1]
    foodImage = base64.b64decode(foodImage)

    user = User.query.get(userId)

    new_food = Food(foodName = foodName, foodImage=foodImage ,foodNation = foodNation, foodTime = foodTime, foodDescription = foodDescription, servingFor = servingFor, user = user)
    try:
        db.session.add(new_food)
        db.session.commit()
        response_data = {
            "message": "User registered successfully",
        }
        return jsonify(response_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500