# create_tables.py
from app import app
from app.extensions.db import db

with app.app_context():
    db.drop_all()
    db.create_all()
