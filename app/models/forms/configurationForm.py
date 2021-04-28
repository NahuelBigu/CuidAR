from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email, NumberRange

class ConfigurationForm(FlaskForm):
    title= StringField('Titulo',validators=[InputRequired('El titulo no puede estar vacio!')])
    description= TextAreaField('Descripcion', validators=[InputRequired('Es necesario que exista una descripcion!')])
    email= StringField('Email', validators=[InputRequired('Es necesario que exista un contacto!'),Email('Es necesesario que el campo sea un Email!')])
    elementsPerPage= IntegerField('Elementos por pagina', validators=[InputRequired('Es necesario ingresar un Numero entre 3 y 40!'), NumberRange(min=3,max=40,message='El numero de elementos debe estar entre 3 y 40!')])
    habilitate= BooleanField('Pagina Habilitada')