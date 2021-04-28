from wtforms import StringField, PasswordField, validators, BooleanField, SelectMultipleField, HiddenField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, InputRequired, Length, AnyOf, Email, DataRequired
from flask_wtf import FlaskForm
from app.models.user import User
from app.models.role import Role

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('A email is required'), Email()])
    password = PasswordField('Contraseña', validators=[InputRequired('Password is required!')])
class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[InputRequired('Nombre de usuario no puede ser vacio!'), Length(min=5, max=20, message='El usuario tiene que tener como minimo 5 letras y como maximo 20.')])
    password = PasswordField('Contraseña', validators=[InputRequired('Contraseña no puede ser vacio!')])
    email = StringField('Email', validators=[InputRequired('Email no puede ser vacio!'), Email()])
    first_name = StringField('Nombre', validators=[InputRequired('Nombre no puede ser vacio!')])
    last_name = StringField('Apellido', validators=[InputRequired('Apellido no puede ser vacio!')])
    active = BooleanField('Activo')
    image = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'], 'Solo imagenes!')])
    #rols=[(rol.id,rol.name) for rol in Role.all()]
    roles= SelectMultipleField('Roles',choices= [], coerce= int)

    def validate_username(self, username):
        if User.validate_username(username.data):
            raise ValidationError('Porfavor use un nombre de usuario diferente.')

    def validate_email(self, email):
        if User.validate_email(email.data):
            raise ValidationError('Porfavor use un email diferente.')

    
class EditForm(FlaskForm):
    user_id = HiddenField('user_id', validators=[InputRequired()])
    username = StringField('Nombre de usuario', validators=[InputRequired('Nombre de usuario no puede ser vacio!'), Length(min=5, max=20, message='El usuario tiene que tener como minimo 5 letras y como maximo 20.')])
    #password = PasswordField('password', validators=[InputRequired('Password is required!')])
    email = StringField('Email', validators=[InputRequired('Email no puede ser vacio!'), Email()])
    first_name = StringField('Nombre', validators=[InputRequired('Nombre no puede ser vacio!')])
    last_name = StringField('Apellido', validators=[InputRequired('Apellido no puede ser vacio!')])
    active = BooleanField('Activo')
    image = FileField('Imagen', validators=[FileAllowed(['jpg', 'png'], 'Solo imagenes!')])
    roles= SelectMultipleField('Roles',choices= [], coerce= int )

    def validate_username(self, username):
        user=User.find_by_id(self.user_id.data)
        if username.data!=user.username: 
            if User.validate_username(username.data):
                raise ValidationError('Porfavor use un nombre de usuario diferente.')

    def validate_email(self, email):
        user=User.find_by_id(self.user_id.data)
        if email.data!=user.email: 
            if User.validate_email(email.data):
                raise ValidationError('Porfavor use un email diferente.')
    
