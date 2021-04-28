from app.db import db

class TypeCenter(db.Model):
    __tablename__ = 'typecenter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
   
    @classmethod
    def all(cls):
        types = TypeCenter.query.all()
        return types
    
    @classmethod
    def allTuples(cls):
        types = TypeCenter.all()
        types_centers=[(int(_type.id),_type.name) for _type in types]
        return types_centers