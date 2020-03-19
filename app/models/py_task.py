"""
    This file defines database models
"""
from app import db

class PyTask(db.Model):
    """
        Custom Task model
    """
    id = db.Column(db.String(36), primary_key=True)
    url = db.Column(db.String(255))
    path = db.Column(db.String(255))
    type = db.Column(db.String(255))

    def __repr__(self):
        return f"Task id:{self.id} url:{self.url} path:{self.path} type:{self.type}"
