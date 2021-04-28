from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.configuration import Configuration 
from app.models.forms.configurationForm import ConfigurationForm
from app.helpers.control_decorator import control
from app.helpers.permission import check as has_permission

@control
def config():
    if not has_permission(session,"config_index"): # Check permission
        return redirect(url_for("home")) 
    con=Configuration.last()
    form=ConfigurationForm()
    form.description.data=con.description
    return render_template("config/config.html", config=con, form=form)


@control
def add():
    if not has_permission(session,"config_new"): # Check permission
        return redirect(url_for("home")) 

    form=ConfigurationForm()
    if form.validate_on_submit():
        flash("Se actualizo la configuracion",category="success")
        con=Configuration.create(form)
    else: con=Configuration.last()
    return render_template("config/config.html", config=con, form=form)