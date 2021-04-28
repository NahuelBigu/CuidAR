from app.db import db
from app.models import permission

role_permission = db.Table('role_permission',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    permission = db.relationship('Permission', secondary=role_permission, backref=db.backref('roles', lazy='dynamic'))

    def __init__ (self ,name):
        self.name=name

    def has_permission(self , permission):
        for perm in self.permission:              #Busco todos los permisos del rol
            if(perm.name == permission):
                return True
    @classmethod
    def all(cls):
        roles = Role.query.all()
        return roles

    @classmethod
    def allTuples(cls):
        roles = Role.query.all()
        rols=[(int(rol.id),rol.name) for rol in roles]
        return rols
    