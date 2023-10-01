from app.extensions.db import db
from app.models.foodhashtag_model import FoodHashtag
from flask import Blueprint, jsonify, request

foodhashtag_bp = Blueprint('foodhashtag_bp', __name__)


