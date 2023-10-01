from app.extensions.db import db
from app.models.user_model import User
from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/auth/login', methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        response_data = {
            'message': 'Login successful',
            'id': user.id,
            'username': user.username,
        }
        return jsonify(response_data), 200 
    else:
        error_data = {'message': 'Login failed'}
        return jsonify(error_data), 401 

@auth_bp.route('/api/auth/signup/', methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    # existing_user = User.query.filter_by(username=username).first()

    # if existing_user:
    #     error_data = {"message": "Username already exists"}
    #     return jsonify(error_data), 400
    
    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    response_data = {
        "message": "User registered successfully",
        "user_id": new_user.id
    }
    return jsonify(response_data), 201