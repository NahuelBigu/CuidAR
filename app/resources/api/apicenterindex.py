from flask import jsonify, request
from flask_restful import Resource, abort
from flask_wtf import FlaskForm
from app.models.helpcenter import HelpCenter
from app.helpers.centerToDictionary import dictionaryPerPage, toDictionary
from app.models.configuration import Configuration
from app.models.forms.helpcenter import HelpCenterNewForm
from app.models.typecenter import TypeCenter
import requests
import os
from app.models.turn import Turn
class Api_center_index(Resource):

    def get(self):
       
        page = request.args.get("page")
        if not page:
            page=1
        con= Configuration.last()
        cantAux= con.elementsPerPage if (not request.args.get("perPage")) else request.args.get("perPage") 
        centers=HelpCenter.allAccepted(int(page), int(cantAux))
        cant=HelpCenter.cant()
        return jsonify(dictionaryPerPage(centers,cant,page))

    def post(self):
        
       
        form = HelpCenterNewForm(csrf_enabled=False)
        types = TypeCenter.allTuples()
        form.type_center.choices = types
        municipios = requests.get(
            'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
        municipios = dict(municipios.json())['data']['Town']
        municipios = [(int(municipio['id']), municipio['name'])
                      for municipio in municipios.values()]
        form.municipio.choices = municipios
        if form.validate_on_submit():
            center = HelpCenter.create(form)
            filename = None
            if 'view_protocol' in request.files:
                file = request.files['view_protocol']
                if file:
                    filename = str(center.id)+"-Protocolo.pdf"
                    file.save(os.path.join('app/static/uploads', filename))
            center.addFileName(filename)
            return jsonify(toDictionary(center))
        abort(400,  message=form.errors)
