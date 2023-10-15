from app.extensions.db import db
from app.models.comment_model import Comment
from app.models.user_model import User
from app.models.food_model import Food
from flask import Blueprint, jsonify, request

comment_bp = Blueprint("comment_bp", __name__)


@comment_bp.route("/api/comment/getByfoodId", methods=["GET"])
def getCommentByFoodId():
    foodId = request.args.get("foodId")
    comments = Comment.query.filter_by(foodId=foodId).all()
    food = food.query.get(foodId)

    if food is None:
        return jsonify({"error": "food not found"}), 404

    comment_list = []
    for comment in comments:
        comment = {
            "userId": comment.userId,
            "foodId": comment.foodId,
            "commentContent": comment.commentContent,
        }
        comment_list.append(comment)

    response_data = {"comment": comment_list}

    return jsonify(response_data), 200


@comment_bp.route("/api/comment/create", methods=["POST"])
def create_food():
    userId = request.json.get("userId")
    foodId = request.json.get("foodId")
    commentContent = request.json.get("commentContent")

    user = User.query.get(userId)
    food = Food.query.get(foodId)
    new_comment = Comment(user=user, food=food, commentContent=commentContent)
    try:
        db.session.add(new_comment)
        db.session.commit()
        response_data = {
            "message": "Add successfully new food!",
        }
        return jsonify(response_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
