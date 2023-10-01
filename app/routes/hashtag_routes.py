from app.extensions.db import db
from app.models.hashtag_model import Hashtag
from flask import Blueprint, jsonify, request

hashtag_bp = Blueprint('hashtag_bp', __name__)

@hashtag_bp.route('/api/hashtag/getAll/', methods=["GET"])
def get_hashtags():
    hashtags = Hashtag.query.all()
    hashtag_list = [{'id': hashtag.id, 'hashtagName': hashtag.hashtagName} for hashtag in hashtags]
    return jsonify(hashtag_list)

@hashtag_bp.route('/api/hashtag/create/', methods=["POST"])
def create_hashtag():
    hashtagName = request.json.get("hashtagName")
    
    new_hashtag = Hashtag(hashtagName=hashtagName)
    db.session.add(new_hashtag)
    db.session.commit()

    response_data = {
        "message": "User registered successfully",
    }
    return jsonify(response_data), 201
