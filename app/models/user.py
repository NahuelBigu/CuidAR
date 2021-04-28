from app.db import db
from werkzeug.security import generate_password_hash,check_password_hash
from app.models.role import Role

user_role = db.Table('user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    first_name= db.Column(db.String(255), nullable=False)
    last_name= db.Column(db.String(255), nullable=False)
    user_image= db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=user_role,lazy='subquery', backref=db.backref('users', lazy=True))
    id_google= db.Column(db.String(255), nullable=True)
    id_facebook= db.Column(db.String(255), nullable=True)

    def __init__ (self ,email,username,password,first_name,last_name,active,user_image):
        self.email=email
        self.username=username
        self.active=active
        pass_hash = generate_password_hash(password)
        self.password=pass_hash
        self.first_name=first_name
        self.last_name=last_name
        self.user_image=user_image if user_image else "/"

    def __getitem__(self, field):
        return self.__dict__[field]

    def check_password(self, password):
        return check_password_hash(self.password, password)
    def check_not_active(self):
        return not self.active
    @classmethod
    def all(cls):        
        users = User.query.all()
        return users

    @classmethod
    def find(cls, user_id):
        user = User.query.get(user_id)
        return user
        
    def is_admin(self):
        for rol in self.roles:
            if (rol.id == 1):
                return True
        return False   

    def is_active(self):
        return self.active
        
    @classmethod
    def validate_admin(cls, user_id):
        user = User.query.get(user_id)
        return user.is_admin();   

    @classmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username).first()
        return user is not None
        
    @classmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user is not None
           
    
    @classmethod
    def create(cls, form):
        user= User(email=form.email.data,username=form.username.data,password=form.password.data,first_name=form.first_name.data,last_name=form.last_name.data,user_image=form.image.data,active=form.active.data)
        
        rolesData=[int(rol) for rol in form.roles.data]
        roles=Role.query.filter(Role.id.in_(rolesData)).all()
        user.roles.extend(roles)

        db.session.add(user)
        db.session.commit()


    
    @classmethod
    def login(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return False
            ##flash('Invalid username or password')
            ##return redirect(url_for('login'))
        return user

    @classmethod
    def has_permission(cls ,user_id,permission):
        #chequear si tiene el permiso
        user=User.query.get(user_id)
        for rol in user.roles if (user) else [] :    #para todos los roles
            if(rol.has_permission(permission)):
                return True
        return False


    @classmethod
    def find_by_id(self, user_id):
        user = User.query.get(user_id)
        return user

    @classmethod    
    def find_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        return user
        
    @classmethod    
    def find_by_id_social(self, id,social):
        user=None
        if (social=="google"):
            user = User.query.filter_by(id_google=id).first()
        elif (social=="facebook"):
            user = User.query.filter_by(id_facebook=id).first()
        return user
    def saveSocialLink(self,id,social):
        if (social=="google"):
            self.id_google=id
        elif (social=="facebook"):
            self.id_facebook=id
        db.session.commit()
    
    def deleteSocialLink(self,social):
        if (social=="google"):
            self.id_google=None
        elif (social=="facebook"):
            self.id_facebook=None
        db.session.commit()
        
    @classmethod
    def activate(cls,user_id):
        user=cls.find_by_id(user_id)
        if user==None: return None
        user.active=True
        db.session.commit()
        return user

    @classmethod
    def deactivate(cls,user_id):
        user=cls.find_by_id(user_id)
        if user==None: return None
        user.active=False
        db.session.commit()
        return user
    
    @classmethod
    def delete_user(cls,user_id):
        user=User.find_by_id(user_id)
        print(user)
        if user is None: return None
        db.session.delete(user)
        db.session.commit()
        return user

    @classmethod
    def edit_us(cls,form):
        u=cls.find_by_id(form.user_id.data)        
        rolesData=form.roles.data
        roles=Role.query.filter(Role.id.in_(rolesData)).all()
        u.roles=roles
        u.email=form.email.data
        u.username=form.username.data
        u.first_name=form.first_name.data
        u.last_name=form.last_name.data
        u.user_image=form.image.data
        u.active=form.active.data
        db.session.commit()
        return u


