# app/__init__.py
from flask import Flask
from app.extensions.db import db

app = Flask(__name__)
app.config.from_object('config.config')

db.init_app(app)

from app.routes import user_routes  
app.register_blueprint(user_routes.user_bp)

from app.routes import auth_routes
app.register_blueprint(auth_routes.auth_bp)


from app.routes import food_routes
app.register_blueprint(food_routes.food_bp)

from app.routes import ingredient_routes
app.register_blueprint(ingredient_routes.ingredient_bp)

from app.routes import hashtag_routes
app.register_blueprint(hashtag_routes.hashtag_bp)

from app.routes import comment_routes
app.register_blueprint(comment_routes.comment_bp)

from app.routes import foodhashtag_routes
app.register_blueprint(foodhashtag_routes.foodhashtag_bp)

from app.routes import making_routes
app.register_blueprint(making_routes.making_bp)
