from app.extensions.db import db

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class Hashtag(db.Model):
    __tablename__ = 'hashtags'

    hashtagId = db.Column(db.Integer, primary_key=True)
    hashtagName = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, hashtagName):
        self.hashtagName = hashtagName 
