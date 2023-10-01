from app.extensions.db import db
from app.models.comment_model import Comment
from flask import Blueprint, jsonify, request

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/api/comment/getByfoodId', methods = ['GET'])
def getCommentByFoodId():
    foodId = request.args.get('foodId')
    comments = Comment.query.filter_by(foodId=foodId).all()
    food = food.query.get(foodId)

    if food is None:
        return jsonify({"error": "food not found"}), 404

    comment_list = []
    for comment in comments:
        comment = {
            "userId": comment.userId,
            "foodId": comment.foodId,
            "commentContent": comment.commentContent
        }
        comment_list.append(comment)

    response_data = {
        "comment": comment_list
    }

    return jsonify(response_data), 200