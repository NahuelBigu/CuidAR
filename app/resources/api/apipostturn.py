from flask import jsonify, request
from flask_restful import Resource, abort
from flask_wtf import FlaskForm
from datetime import time, timedelta
from datetime import date
from app.models.helpcenter import HelpCenter
from app.models.turn import Turn
from app.helpers.turntodictionary import listOfTurns, turnToDictionary
from app.helpers.turn import all_turns3
from app.models.forms.turn import ApiTurnNewForm
import requests

class Api_post_turn(Resource):

    def post(self, idcentro):
        form= ApiTurnNewForm(csrf_enabled=False)
        if not HelpCenter.isAccepted(form.centro_id.data):
            abort(404, message={ 'Fecha' : 'Fecha erronea'})
        if form.validate_on_submit():
            center=HelpCenter.find(form.centro_id.data)
            t=str(form.hora_inicio.data)
            if validate_time(time(hour=int(t[0:2]),minute=int(t[3:5])),form.centro_id.data,str(form.fecha.data)):
                turn=Turn.apiCreate(form)
                return jsonify(turnToDictionary(turn))
        abort(404, message=form.errors)

def validate_time(ot, idc, fecha):
    turnosd=all_turns3(idc, fecha.replace('-',''))
    if str(ot) in turnosd:
        return True
    return False