import base64
from app.utils.CoverImage import ConverBase64ToImage, DecodeBase64, ConverImageToBase64
from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.user_model import User
from app.models.food_model import Food

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    print(username, password)
    user_data = User.query.filter_by(username=username, password=password).first()
    # print(ConverBase64ToImage(user_data.avatar))
    try:
        if user_data:
            foods_data = Food.query.filter_by(user_id=user_data.id).all()
            foods_res = []
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
            response_data = {
                "userId": user_data.id,
                "username": user_data.username,
                "pycookID": user_data.pycookID,
                "avatar": ConverBase64ToImage(user_data.avatar),
                "fullname": user_data.fullname,
                "foods": foods_res,
            }
            return jsonify(response_data), 200
        else:
            error_data = {"message": "Login failed"}
            return jsonify(error_data), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/api/auth/signup/", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    pycoodID = request.json.get("pycookID")
    avatar = DecodeBase64(request.json.get("avatar"))
    fullname = request.json.get("fullname")

    try:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_data = {"message": "Username already exists"}
            return jsonify(error_data), 400

        new_user = User(
            username=username,
            password=password,
            pycookID=pycoodID,
            fullname=fullname,
            avatar=avatar,
        )
        db.session.add(new_user)
        db.session.commit()
        response_data = {
            "message": "User registered successfully",
            "user_id": new_user.id,
        }
        return jsonify(response_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
