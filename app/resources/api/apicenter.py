from flask import jsonify, request
from flask_restful import Resource, abort
from app.models.helpcenter import HelpCenter
from app.helpers.centerToDictionary import toDictionary
from app.models.forms.helpcenter import HelpCenterNewForm

class  Api_center(Resource):
    
    def get(self, centerid):
        center=HelpCenter.find(centerid)
        if not center:
            abort(404, message= "No se puede encontrar el centro de ayuda")
        return jsonify(toDictionary(center))