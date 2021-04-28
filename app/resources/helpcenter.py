from flask import redirect, render_template, request, url_for, session, abort, flash,send_file ,send_from_directory 
from werkzeug.utils import secure_filename
from app.models.helpcenter import HelpCenter
from app.models.typecenter import TypeCenter
from app.models.configuration import Configuration
from app.helpers.control_decorator import control
from app.helpers.permission import check as has_permission
from app.models.forms.helpcenter import EditHelpCenterForm, HelpCenterNewForm
import requests
from io import BytesIO
import os

# Protected resources


@control
def index():
    if not has_permission(session, "helpcenter_index"):  # Check permission
        return redirect(url_for("home"))
    municipios = requests.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
    municipios=dict(municipios.json())['data']['Town']
    municipios2={}
    for municipio in municipios.values():
        municipios2[int(municipio['id'])]=municipio['name']
    
    elementsPerPage = Configuration.last().elementsPerPage
    helpcenters = HelpCenter.all()
    return render_template("helpcenter/index.html", helpcenters=helpcenters, elementsPerPage=elementsPerPage,municipios=municipios2)


@control
def new():
    if not has_permission(session, "helpcenter_new"):  # Check permission
        return redirect(url_for("home"))

    form = HelpCenterNewForm()
    types = TypeCenter.allTuples()
    form.type_center.choices = types

    municipios = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
    municipios = dict(municipios.json())['data']['Town']
    municipios = [(int(municipio['id']), municipio['name'])
                  for municipio in municipios.values()]
    form.municipio.choices = municipios

    return render_template("helpcenter/new.html", form=form)


@control
def create():
    if not has_permission(session, "helpcenter_new"):  # Check permission
        return redirect(url_for("home"))
    form = HelpCenterNewForm()
    types = TypeCenter.allTuples()
    form.type_center.choices = types
    municipios = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
    municipios = dict(municipios.json())['data']['Town']
    municipios = [(int(municipio['id']), municipio['name'])
                  for municipio in municipios.values()]
    form.municipio.choices = municipios
    if form.validate_on_submit():
        helpcenter = HelpCenter.create(form)
        filename=None
        if 'view_protocol' in request.files:
            file = form.view_protocol.data
            if file:
                filename = str(helpcenter.id)+"-Protocolo.pdf"
                APP_ROOT = os.path.dirname(os.path.abspath(__file__))
                UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
                file.save(os.path.join(UPLOAD_FOLDER.replace("/resources",""), filename))                
        helpcenter.addFileName(filename)
        flash("Se creo el centro de ayuda \"" +
              str(form.name.data)+"\"", category="success")
        return redirect(url_for("helpcenter_index"))

    return render_template("helpcenter/new.html", form=form)


@control
def accept(helpcenter_id):
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))
    HelpCenter.accepted(helpcenter_id)
    return redirect(url_for("helpcenter_index"))


@control
def reject(helpcenter_id):
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))
    HelpCenter.reject(helpcenter_id)
    return redirect(url_for("helpcenter_index"))


@control
def publish(helpcenter_id):
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))
    HelpCenter.publish(helpcenter_id)
    return redirect(url_for("helpcenter_index"))


@control
def unpublish(helpcenter_id):
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))
    HelpCenter.unpublish(helpcenter_id)
    return redirect(url_for("helpcenter_index"))


@control
def delete(helpcenter_id):
    if not has_permission(session, "helpcenter_delete"):  # Check permission
        return redirect(url_for("home"))
    HelpCenter.delete(helpcenter_id)
    flash('Centro de ayuda eliminado correctamente', category="success")
    return redirect(url_for("helpcenter_index"))


@control
def edit(helpcenter_id):  # PREGUNTAR COMO CAMBIAR LA RUTA PARA QUE NO SE MUESTRE EL ID SINO EL NOMBRE , VER SI NOMBRE ES UNICO O NO TODO
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))
    helpcenter = HelpCenter.find(helpcenter_id)
    if helpcenter is None:  # Check helpcenter
        return redirect(url_for("home"))

    form = EditHelpCenterForm(obj=helpcenter)
    form.helpcenter_id.data = helpcenter.id
    types = TypeCenter.allTuples()
    form.type_center.choices = types
    form.type_center.data = [int(typecenter.id)
                             for typecenter in helpcenter.type_center]

    municipios = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')

    municipios = dict(municipios.json())['data']['Town']
    municipios = [(municipio['id'], municipio['name'])
                  for municipio in municipios.values()]
    form.municipio.choices = municipios

    return render_template("helpcenter/edit.html", form=form, types=types, helpcenter=helpcenter)


@control
def post_edit():
    if not has_permission(session, "helpcenter_update"):  # Check permission
        return redirect(url_for("home"))

    form = EditHelpCenterForm()
    helpcenter = HelpCenter.find(form.helpcenter_id.data)
    types = TypeCenter.allTuples()
    form.type_center.choices = types

    municipios = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?per_page=150')
    municipios = dict(municipios.json())['data']['Town']
    municipios = [(int(municipio['id']), municipio['name'])
                  for municipio in municipios.values()]
    form.municipio.choices = municipios

    if form.validate_on_submit():
        flash("Centro de ayuda editado correctamente", category="success")
        HelpCenter.edit(form)
        filename=None
        if 'view_protocol' in request.files:
            file = form.view_protocol.data
            if file:
                filename = str(helpcenter.id)+"-Protocolo.pdf"
                file.save(os.path.join('./app/static/uploads', filename)) 
        if (helpcenter.view_protocol != None):
            os.remove('./app/static/uploads/'+ helpcenter.view_protocol)          
        helpcenter.addFileName(filename)
        return redirect(url_for("helpcenter_index"))
    form.helpcenter_id.data = helpcenter.id
    form.type_center.data = [int(typecenter.id)
                             for typecenter in helpcenter.type_center]
    return render_template("helpcenter/edit.html", form=form, types=types, helpcenter=helpcenter)

    form.types.data = [int(typecenter.id)
                       for typecenter in helpcenter.type_center]
    return render_template("helpcenter/edit.html", form=form, types=types, helpcenter=helpcenter)

@control
def download_pdf(helpcenter_id):
    helpcenter=HelpCenter.find(helpcenter_id)
    if helpcenter is None: # Check helpcenter
        return redirect(url_for("home"))
    filename=helpcenter.view_protocol

    return redirect("/static/uploads/"+filename)
    #return send_file(BytesIO(helpcenter.view_protocol), attachment_filename=name, as_attachment=True)