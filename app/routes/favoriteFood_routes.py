from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.favoriteFood_model import FavoriteFood
from app.models.user_model import User
from app.models.food_model import Food


favoriteFood_bp = Blueprint("favoriteFood", __name__)


@favoriteFood_bp.route("/api/favoriteFood/create", methods=["GET"])
def CreateFavoriteFood():
    userId = request.args.get("userId")
    foodId = request.args.get("foodId")

    try:
        existing_favorite = FavoriteFood.query.filter_by(
            userId=userId, foodId=foodId
        ).first()

        if existing_favorite:
            db.session.delete(existing_favorite)
            db.session.commit()
            return jsonify("Food already exists"), 200
        else:
            user = User.query.filter_by(id=userId).first()
            food = Food.query.filter_by(foodId=foodId).first()

            new_favorite_food = FavoriteFood(user, food)
            db.session.add(new_favorite_food)
            db.session.commit()
            return jsonify("Save favorite food"), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@favoriteFood_bp.route("/api/favoriteFood/hasSavedFood", methods=["GET"])
def hasSavedFood():
    userId = request.args.get("userId")
    foodId = request.args.get("foodId")

    try:
        favorite_food = FavoriteFood.query.filter_by(
            userId=userId, foodId=foodId
        ).first()
        if favorite_food:
            return jsonify("has saved food"), 200
        else:
            return jsonify("has not saved food"), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
