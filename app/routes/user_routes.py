from app.extensions.db import db
from app.models.user_model import User
from app.models.food_model import Food
from app.utils.CoverImage import ConverBase64ToImage, DecodeBase64, ConverImageToBase64
from flask import Blueprint, jsonify, request

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/api/user/getById", methods=["GET"])
def getById():
    userId = request.args.get("userId")
    user_data = User.query.get(userId)

    if user_data is None:
        return jsonify({"error": "User not found"}), 404
    else:
        foods_data = Food.query.filter_by(user_id=user_data.id).all()
        foods_res = []
        favorite_foods_res = []
        for food in foods_data:
            foods_res.append(
                {
                    "foodId": food.foodId,
                    "foodImage": ConverImageToBase64(food.foodImage),
                    "foodName": food.foodName,
                    "likeTotal": food.likeTotal,
                    "heartTotal": food.heartTotal,
                    "deliciousTotal": food.deliciousTotal,
                }
            )

        for favorite_food in user_data.favourite_foods:
            favorite_foods_res.append(
                {
                    "foodId": favorite_food.food.foodId,
                    "foodImage": ConverImageToBase64(favorite_food.food.foodImage),
                    "foodName": favorite_food.food.foodName,
                    "likeTotal": favorite_food.food.likeTotal,
                    "heartTotal": favorite_food.food.heartTotal,
                    "deliciousTotal": favorite_food.food.deliciousTotal,
                }
            )

        response_data = {
            "userId": user_data.id,
            "username": user_data.username,
            "pycookID": user_data.pycookID,
            "avatar": ConverBase64ToImage(user_data.avatar),
            "fullname": user_data.fullname,
            "foods": foods_res,
            "favorite_foods": favorite_foods_res,
            "followerTotal": len(user_data.followers),
            "followedByTotal": len(user_data.followedBy),
        }
        return jsonify(response_data), 200
