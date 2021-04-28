from app.db import db

class Permission(db.Model):
    __tablename__ = 'permission'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    
    def __init__ (self ,name):
        self.name=name