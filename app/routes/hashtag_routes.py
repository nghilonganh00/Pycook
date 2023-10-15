from app.extensions.db import db
from app.models.hashtag_model import Hashtag
from flask import Blueprint, jsonify, request

hashtag_bp = Blueprint('hashtag_bp', __name__)

@hashtag_bp.route('/api/hashtag/getAll/', methods=["GET"])
def getAllHashtags():
    hashtags = Hashtag.query.all()
    hashtag_list = [{'hashtagName': hashtag.hashtagName} for hashtag in hashtags]
    return jsonify(hashtag_list), 200

@hashtag_bp.route('/api/hashtag/create/', methods=["POST"])
def createNewHashtag():
    hashtagName = request.json.get("hashtagName")

    existHashtag = Hashtag.query.filter_by(hashtagName=hashtagName).all()
    if existHashtag:
        return jsonify({"message": f"This hashtag '{hashtagName}' does not exist."}), 404
    
    new_hashtag = Hashtag(hashtagName=hashtagName)
    try:
        db.session.add(new_hashtag)
        db.session.commit()

        response_data = {
            "message": "Create new hashtag successfully",
        }
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
   
