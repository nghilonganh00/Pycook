from app.extensions.db import db
from flask import Blueprint, jsonify, request

from app.models.making_model import Making
from app.models.food_model import Food

import base64
making_bp = Blueprint('making_bp', __name__)

@making_bp.route('/api/making/getAll', methods=['GET'])
def getMakingByFoodIs():
    foodId = request.args.get("foodId")
    food = Food.query.get(foodId)  
    