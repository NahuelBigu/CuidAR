from flask import jsonify, request
from flask_restful import Resource, abort
from flask_wtf import FlaskForm
from datetime import date
from app.models.helpcenter import HelpCenter
from app.models.turn import Turn
from app.helpers.turntodictionary import listOfTurns
import requests


class Api_turn_index(Resource):

    def get(self, idcentro):
        center = HelpCenter.find(idcentro)
        if not center:
            abort(400, message= 'no se encuentra el centro')
        r = request.args.get("fecha")
        if r:
            if len(r)==10:
                da=str(r)
                d = date(year=int(da[0:4]), month=int(da[5:7]),day=int(da[8:10]))
            else:
                d = date.today()
        else:
            d = date.today()
        return jsonify(listOfTurns(center, d))
