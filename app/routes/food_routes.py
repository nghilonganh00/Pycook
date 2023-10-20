import base64
from app.extensions.db import db
from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from app.models.food_model import Food
from app.models.user_model import User
from app.models.making_model import Making
from app.models.follower_model import Follower

from app.utils.CoverImage import (
    ConverBase64ToImage,
    ConverImageToBase64,
    ConverBase64ToPath,
)

food_bp = Blueprint("food_bp", __name__)


@food_bp.route("/api/food/getAll", methods=["GET"])
def getAllFood():
    # Lấy ra 20 món ăn đầu tiên
    food_data = Food.query.limit(20).all()

    response_data = []
    for food in food_data:
        chef = {
            "pycookID": food.user.pycookID,
            "fullname": food.user.fullname,
            "avatar": ConverBase64ToImage(food.user.avatar),
            "username": food.user.username,
        }

        response_food = {
            "foodId": food.foodId,
            "chef": chef,
            "foodName": food.foodName,
            "foodImage": ConverImageToBase64(food.foodImage),
            "foodNation": food.foodNation,
            "foodTime": food.foodTime,
            "foodDescription": food.foodDescription,
            "servingFor": food.servingFor,
            "deliciousTotal": food.deliciousTotal,
            "heartTotal": food.heartTotal,
            "likeTotal": food.likeTotal,
            "created_at": food.created_at,
        }
        food.viewTotal += 1
        db.session.commit()
        response_data.append(response_food)

    return jsonify(response_data), 200


@food_bp.route("/api/food/getByIngredientName", methods=["GET"])
def getFoodByIngredientName():
    ingredient_name_to_query = request.args.get("ingredientName")
    try:
        foods = Food.query.filter(
            Food.recipes.ilike(f"%{ingredient_name_to_query}%")
        ).all()
        result = []
        print(ingredient_name_to_query.encode("unicode-escape").decode("utf-8"))
        for food in foods:
            chef = {
                "pycookID": food.user.pycookID,
                "fullname": food.user.fullname,
                "avatar": ConverBase64ToImage(food.user.avatar),
            }

            food_res = {
                "foodId": food.foodId,
                "foodName": food.foodName,
                "foodImage": ConverImageToBase64(food.foodImage),
                "heartTotal": food.heartTotal,
                "likeTotal": food.likeTotal,
                "deliciousTotal": food.deliciousTotal,
                "created_at": food.created_at,
                "chef": chef,
            }
            result.append(food_res)
            print(food.recipes)
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@food_bp.route("/api/food/getByFoodId", methods=["GET"])
def getFoodByFoodId():
    foodId = request.args.get("foodId")
    food = Food.query.get(foodId)

    if food:
        comments_data = food.comments
        makings_data = food.makings
        chef = {
            "id": food.user.id,
            "pycookID": food.user.pycookID,
            "fullname": food.user.fullname,
            "avatar": ConverBase64ToImage(food.user.avatar),
        }

        makings_res = []
        comments_res = []

        for making in makings_data:
            makings_res.append(
                {
                    "makingOrder": making.makingOrder,
                    "makingContent": making.makingContent,
                }
            )

        for comment in comments_data:
            comments_res.append(
                {
                    "userAvatar": ConverBase64ToImage(comment.user.avatar),
                    "userFullname": comment.user.fullname,
                    "userPycookId": comment.user.pycookID,
                    "content": comment.commentContent,
                }
            )

        result = {
            "foodId": food.foodId,
            "chef": chef,
            "comments": comments_res,
            "foodName": food.foodName,
            "foodImage": ConverImageToBase64(food.foodImage),
            "foodNation": food.foodNation,
            "foodTime": food.foodTime,
            "recipes": food.recipes.split("%&"),
            "makings": makings_res,
            "foodDescription": food.foodDescription,
            "servingFor": food.servingFor,
            "deliciousTotal": food.deliciousTotal,
            "heartTotal": food.heartTotal,
            "likeTotal": food.likeTotal,
            "created_at": food.created_at,
        }
        food.viewTotal += 1
        db.session.commit()
        return jsonify(result), 200
    else:
        return jsonify("Khong tim thay food"), 404


@food_bp.route("/api/food/getFoodByName", methods=["GET"])
def getFoodByName():
    search_name = request.args.get("searchName")

    try:
        foods = Food.query.filter(Food.foodName.ilike(f"%{search_name}%")).all()
        result = []
        for food in foods:
            chef = {
                "pycookID": food.user.pycookID,
                "fullname": food.user.fullname,
                "avatar": ConverBase64ToImage(food.user.avatar),
            }

            food_res = {
                "foodId": food.foodId,
                "foodName": food.foodName,
                "foodImage": ConverImageToBase64(food.foodImage),
                "recipes": food.recipes.split("%&"),
                "chef": chef,
            }
            result.append(food_res)
        return jsonify(result), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@food_bp.route("/api/food/getLastestByUserId", methods=["GET"])
def getLastestByUserId():
    userId = request.args.get("userId")
    try:
        foods_data = (
            Food.query.filter_by(user_id=userId)
            .order_by(desc(Food.created_at))
            .limit(4)
            .all()
        )
        foods_res = []

        for food in foods_data:
            foods_res.append(
                {
                    "foodId": food.foodId,
                    "foodName": food.foodName,
                    "foodImage": food.foodImage,
                }
            )
        return jsonify(foods_res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@food_bp.route("/api/food/getLastestByFollowed", methods=["GET"])
def getLastestByFollowed():
    userId = request.args.get("userId")
    user_data = User.query.filter_by(id=userId).first()
    followed_users = (
        db.session.query(User, Food)
        .join(Follower, Follower.followedId == User.id)
        .join(Food, Food.user_id == User.id)
        .filter(Follower.followerId == user_data.id)
        .order_by(Food.created_at.desc())
        .group_by(User.id)
        .order_by(Food.created_at.desc())
        .distinct(User.id)
        .all()
    )

    foods_res = []

    for user, food in followed_users:
        foods_res.append(
            {
                "chef": {
                    "userId": user.id,
                    "avatar": user.avatar,
                    "fullname": user.fullname,
                },
                "food": {
                    "foodId": food.foodId,
                    "foodName": food.foodName,
                    "foodImage": ConverImageToBase64(food.foodImage),
                    "foodDescription": food.foodDescription,
                    "likeTotal": food.likeTotal,
                    "heartTotal": food.heartTotal,
                    "deliciousTotal": food.deliciousTotal,
                },
            }
        )
    # Bước 1: Lấy danh sách người đã theo dõi
    # followed_users = (
    #     db.session.query(User)
    #     .join(Follower, Follower.followedId == User.id)
    #     .filter(Follower.followerId == user_data.id)
    #     .all()
    # )

    # # Bước 2: Lấy món ăn mới nhất của từng người đã theo dõi
    # latest_foods = []
    # for followed_user in followed_users:
    #     latest_food = (
    #         db.session.query(Food)
    #         .filter(Food.user_id == followed_user.id)
    #         .order_by(Food.created_at.desc())
    #         .first()
    #     )
    #     if latest_food:
    #         latest_foods.append((followed_user, latest_food))

    return jsonify(foods_res), 200


@food_bp.route("/api/food/create", methods=["POST"])
def create_food():
    userId = request.json.get("userId")
    foodName = request.json.get("foodName")
    foodNation = request.json.get("foodNation")
    foodTime = request.json.get("foodTime")
    recipes = request.json.get("recipes")
    makings = request.json.get("makings")
    foodDescription = request.json.get("foodDescription")
    servingFor = request.json.get("servingFor")

    foodImage = request.json.get("foodImage").split(",")[1]
    foodImage = ConverBase64ToPath(foodImage)

    try:
        user = User.query.get(userId)
        new_food = Food(
            foodName=foodName,
            foodImage=foodImage,
            foodNation=foodNation,
            foodTime=foodTime,
            recipes="%&".join(recipes),
            foodDescription=foodDescription,
            servingFor=servingFor,
            user=user,
        )
        db.session.add(new_food)
        db.session.commit()
        makingOrder = 1
        for making in makings:
            new_making = Making(
                food=new_food,
                makingOrder=makingOrder,
                makingContent=making["content"],
                makingImage=making["image"],
            )
            db.session.add(new_making)
            db.session.commit()
            makingOrder += 1

        response_data = {
            "message": "Add successfully new food!",
            "foodId": new_food.foodId,
        }
        return jsonify(response_data), 201
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500


@food_bp.route("/api/food/like", methods=["GET"])
def likeFoodByFoodId():
    foodId = request.args.get("foodId")
    try:
        food = Food.query.get(foodId)
        food.likeTotal += 1
        db.session.commit()
        return jsonify(food.likeTotal), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
