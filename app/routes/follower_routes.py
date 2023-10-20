from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.follower_model import Follower
from app.models.user_model import User
from app.models.food_model import Food


follower_bp = Blueprint("follower", __name__)


@follower_bp.route("/api/follower/create", methods=["GET"])
def CreateFollower():
    followedId = request.args.get("followedId")
    followerId = request.args.get("followerId")

    try:
        existing_follower = Follower.query.filter_by(
            followedId=followedId, followerId=followerId
        ).first()

        if existing_follower:
            db.session.delete(existing_follower)
            db.session.commit()
            return jsonify("Food already exists"), 200
        else:
            new_follower = Follower(followedId=followedId, followerId=followerId)
            db.session.add(new_follower)
            db.session.commit()
            return jsonify("Followed chef"), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@follower_bp.route("/api/follower/hasFollow", methods=["GET"])
def hasSavedFood():
    followedId = request.args.get("followedId")
    followerId = request.args.get("followerId")

    try:
        follower = Follower.query.filter_by(
            followedId=followedId, followerId=followerId
        ).first()
        if follower:
            return jsonify("has followed chef"), 200
        else:
            return jsonify("has not followed chef"), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
