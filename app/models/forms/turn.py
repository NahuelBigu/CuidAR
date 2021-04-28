from wtforms import StringField, SelectField, FloatField, PasswordField, validators, BooleanField, SelectMultipleField, HiddenField, TimeField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import ValidationError, InputRequired, Length, AnyOf, Email, DataRequired
from flask_wtf import FlaskForm
import re


class TurnNewForm(FlaskForm):

    helpcenter_id = HiddenField('helpcenter_id')

    user = StringField('Email', validators=[
        InputRequired('Email no puede ser vacio!'), Email()])

    date = DateField('Fecha de asistencia', validators=[InputRequired(
        'Se debe elegir una fecha a asistir!')])
        
    nombre = StringField('Nombre',validators=[ InputRequired('Nombre no puede ser vacio!')])
    apellido = StringField('Apellido',validators=[InputRequired('Apellido no puede ser vacio!')])

    opening_time = SelectField(
        'Hora de asistencia', validators=[
            InputRequired('Se debe seleccionar hora de asistencia!')])

    phone = StringField('Telefono del donante', validators=[
        InputRequired('telefono no puede ser vacio!')])


class ApiTurnNewForm(FlaskForm):
    centro_id = HiddenField('centro_id')

    email_donante = StringField('email_donante', validators=[
        InputRequired('Email no puede ser vacio!'), Email()])

    nombre = StringField('Nombre',validators=[ InputRequired('Nombre no puede ser vacio!')])
    apellido = StringField('Apellido',validators=[InputRequired('Apellido no puede ser vacio!')])

    fecha = DateField('fecha', validators=[InputRequired(
        'Se debe elegir una fecha a asistir!')])

    hora_inicio = StringField(
        'hora_inicio', validators=[
            InputRequired('Se debe seleccionar hora de asistencia!')])

    telefono_donante = StringField('Telefono del donante', validators=[
        InputRequired('telefono no puede ser vacio!')])
