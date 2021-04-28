from wtforms import StringField,SelectField,FloatField , PasswordField, validators, BooleanField, SelectMultipleField, HiddenField, TimeField
from flask_wtf.file import FileField, FileAllowed, FileRequired 
from wtforms.validators import ValidationError, InputRequired, Length, AnyOf, Email, DataRequired,Optional ,Email
from flask_wtf import FlaskForm
import re

class HelpCenterNewForm(FlaskForm):
    name = StringField('Nombre de Centro', validators=[InputRequired('Nombre de Centro no puede ser vacio!'), Length(min=5, message='El nombre tiene que tener como minimo 5 letras.')])
    address=StringField('Direccion', validators=[InputRequired('La direccion del centro no puede ser vacio!'), Length(min=5, message='La direccion del centro tiene que tener como minimo 5 letras.')])
    phone = StringField('Telefono', validators=[InputRequired('Telefono no puede ser vacio!')])
    opening_time =TimeField('Hora de apertura',validators=[InputRequired('Hora de apertura necesaria!')])
    closing_time =TimeField('Hora de cierre',validators=[InputRequired('Hora de cierre necesaria!')])
    type_center = SelectMultipleField('Tipo de centro de ayuda',choices= [], coerce= int ,validators=[InputRequired('Tipo de centro necesario!')])
    municipio = SelectField('Municipio',validators=[InputRequired('Municipio necesario!')])
    web = StringField('Web',validators=([Optional()]))
    email = StringField('Email',validators=([Optional(), Email()]))
    latitude= FloatField(validators=([InputRequired('Ubicacion necesaria!')]))
    longitude = FloatField(validators=([InputRequired('Ubicacion necesaria!')]))
    view_protocol = FileField('Protocolo de visita (pdf)',validators=[FileAllowed(['pdf'],"Solo se permiten archivos en formato PDF"),Optional() ])
    
    def validate_closing_time(self, closing_time):
        if closing_time.data <= self.opening_time.data:
            raise ValidationError('La fecha de cierre no puede ser anterior a la de apertura.')
        
   
    
class EditHelpCenterForm(FlaskForm):
    helpcenter_id = HiddenField('helpcenter_id', validators=[InputRequired()])
    name = StringField('Nombre de Centro', validators=[InputRequired('Nombre de centro no puede ser vacio!'), Length(min=5, message='El nombre tiene que tener como minimo 5 letras.')])
    address=StringField('Direccion', validators=[InputRequired('La direccion del centro no puede ser vacio!'), Length(min=5, message='La direccion del centro tiene que tener como minimo 5 letras.')])
    phone = StringField('Telefono', validators=[InputRequired('Telefono no puede ser vacio!')])
    opening_time =TimeField('Hora de apertura',validators=[InputRequired('Hora de apertura necesaria!')])
    closing_time =TimeField('Hora de cierre',validators=[InputRequired('Hora de cierre necesaria!')])
    type_center = SelectMultipleField('Tipo de centro de ayuda',choices= [], coerce= int ,validators=[InputRequired('Tipo de centro necesario!')])
    municipio = SelectField('Municipio',validators=[InputRequired('Municipio necesario!')])
    web = StringField('Web',validators=([Optional()]))
    email = StringField('Email',validators=([Optional(),Email()]))   
    latitude= FloatField(validators=([InputRequired('Ubicacion necesaria!')]))
    longitude = FloatField(validators=([InputRequired('Ubicacion necesaria!')]))
    view_protocol = FileField('Protocolo de visita (pdf)',validators=[FileAllowed(['pdf'],"Solo se permiten archivos en formato PDF"),Optional() ])

    def validate_closing_time(self, closing_time):
        if closing_time.data <= self.opening_time.data:
            raise ValidationError('La fecha de cierre no puede ser anterior a la de apertura.')

  
  
