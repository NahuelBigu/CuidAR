from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.user import User
from app.models.configuration import Configuration
from app.models.forms.user import LoginForm


def login():
    form = LoginForm()
    return render_template("auth/login.html",form=form,habilitate=Configuration.last().habilitate)


def authenticate():
    form = LoginForm()

    user = User.login(form.email.data, form.password.data)
    if not user:
        flash("Usuario o clave incorrecto.",category="error")
        return redirect(url_for("auth_login"))
    if user.check_not_active():
        flash("Usuario desactivado.",category="error")
        return redirect(url_for("auth_login"))
    if not user.is_admin() and not Configuration.last().habilitate:
        flash("Pagina deshabilitada",category="error")
        return redirect(url_for("auth_login"))
    session["user_id"] = user["id"]
    session["user_name"] = user["username"]
    flash("La sesión se inició correctamente.",category="success")

    return redirect(url_for("home"))

def deleteSession():
    del session["user_id"]
    del session["user_name"]
    session.clear()
def logout():
    deleteSession()
    flash("La sesión se cerró correctamente.", category="success")
    return redirect(url_for("auth_login"))


#OAUTH LOGIN




def OAuth_facebook_login():
    from app import oauth
    #google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('oauth_facebook_authenticate', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

def OAuth_facebook_autorize():
    from app import oauth

    #google = oauth.create_client('google')  # create the google oauth client
    token = oauth.facebook.authorize_access_token()  # Access token from google (needed to get user info)
    resp = oauth.facebook.get('code')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    
    user_aux = oauth.facebook.userinfo()  # uses openid endpoint to fetch user info

    # Here you use the profile/user data that you got and query your database find/register the user
    
    user = User.find_by_id_social(user_aux["id"],"facebook")
    if not user:
        flash("Cuenta de Facebook incorrecta o no se encuentra vinculada con un usuario del sistema.",category="error")
        return redirect(url_for("auth_login"))
    if user.check_not_active():
        flash("Usuario desactivado.",category="error")
        return redirect(url_for("auth_login"))
    if not user.is_admin() and not Configuration.last().habilitate:
        flash("Pagina deshabilitada",category="error")
        return redirect(url_for("auth_login"))
    session["user_id"] = user["id"]
    session["user_name"] = user["username"]
    flash("La sesión se inició correctamente.",category="success")
    
    return redirect(url_for("home"))







def OAuth_google_login():
    from app import oauth
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('oauth_google_authenticate', _external=True)
    return google.authorize_redirect(redirect_uri)

def OAuth_google_autorize():
    from app import oauth
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = User.find_by_id_social(user_info["id"],"google")
    if not user:
        flash("Cuenta de Gmail incorrecta o no se encuentra vinculada con un usuario del sistema.",category="error")
        return redirect(url_for("auth_login"))
    if user.check_not_active():
        flash("Usuario desactivado.",category="error")
        return redirect(url_for("auth_login"))
    if not user.is_admin() and not Configuration.last().habilitate:
        flash("Pagina deshabilitada",category="error")
        return redirect(url_for("auth_login"))
    session["user_id"] = user["id"]
    session["user_name"] = user["username"]
    flash("La sesión se inició correctamente a travez de Gmail",category="success")
    
    return redirect(url_for("home"))


   
def OAuth_google_link():
    from app import oauth
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('oauth_google_savelink', _external=True)
    return google.authorize_redirect(redirect_uri)

def OAuth_google_saveLink():
    from app import oauth
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = User.find_by_id(session["user_id"])
    if (user and not User.find_by_id_social(user_info["id"],"google")):  #SI YA EXISTE UNA CUENTA VINCULADA NO LA GUARDO
        user.saveSocialLink(user_info["id"],"google")
        flash("Su cuenta se ha linkeado con su cuenta de Gmail",category="success")
    else:
        flash("Ya tiene un usuario vinculado con esa cuenta de Gmail",category="error")
    return redirect(url_for("user_profile"))

def OAuth_google_delete_Link():
    user = User.find_by_id(session["user_id"])
    if (user):
        user.deleteSocialLink("google")
    return redirect(url_for("user_profile"))


def OAuth_facebook_link():
    from app import oauth
    redirect_uri = url_for('oauth_facebook_savelink', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

def OAuth_facebook_saveLink():
    from app import oauth
    token = oauth.facebook.authorize_access_token()  # Access token from google (needed to get user info)
    resp = oauth.facebook.get('code')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    
    user_aux = oauth.facebook.userinfo()  # uses openid endpoint to fetch user info


    user = User.find_by_id(session["user_id"])
    if (user and not User.find_by_id_social(user_aux["id"],"facebook")):  #SI YA EXISTE UNA CUENTA VINCULADA NO LA GUARDO
        user.saveSocialLink(user_aux["id"],"facebook")
        flash("Su cuenta se ha linkeado con su cuenta de Facebook",category="success")
    else:
        flash("Ya tiene un usuario vinculado con esa cuenta de Facebook",category="error")
    return redirect(url_for("user_profile"))

def OAuth_facebook_delete_Link():
    user = User.find_by_id(session["user_id"])
    if (user):
        user.deleteSocialLink("facebook")
    return redirect(url_for("user_profile"))





