from flask import redirect, render_template, request, url_for, session, abort,flash
from app.helpers.auth import authenticated
from app.models.configuration import Configuration
from app.models.user import User
from app.resources.auth import deleteSession
def control(func):
    def wrapper(*args, **kwargs):
        if not authenticated(session):            
            flash("Usted no se encuentra autenticado",category="error")
            return redirect(url_for("home"))   
        user= User.find_by_id(session["user_id"])   
        if not user.is_active(): # Si esta activo o no, si no esta activo le cierra la sesion             
            deleteSession()
            flash("Su cuenta se encuentra desactivada",category="error")
            return redirect(url_for("auth_login"))
        if not user.is_admin():  # Si es admin no le importa si esta habilitado o no  
            if not Configuration.last().habilitate:
                return redirect(url_for("error_message_maintenance"))  
        return func(*args, **kwargs)
    return wrapper
