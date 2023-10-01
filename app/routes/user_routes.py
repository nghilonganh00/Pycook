from app.extensions.db import db
from app.models.user_model import User
from flask import Blueprint, jsonify, request

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/user/get', methods = ['GET'])
def getUserById():
    userId = request.args.get('userId')
    user = User.query.get(userId)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    foods = []
    for food in user.foods:
        food = {
            "id": food.id,
            "foodName": food.foodName,
            "foodNation": food.foodNation,
            "foodTime": food.foodTime,
            "foodDescription": food.foodDescription,
            "servingFor": food.servingFor,
            "deliciousTotal": food.deliciousTotal,
            "heartTotal": food.heartTotal,
            "likeTotal": food.likeTotal,
            "created_at": food.created_at
        }
        foods.append(food)

    response_data = {
        "user_id": user.id,
        "username": user.username,
        "foods": foods
    }

    return jsonify(response_data), 200