from app.helpers import permission as helper_permission
from app.helpers import auth as helper_auth
from app.helpers import handler
from app.resources import home
from app.resources import errorMessage
from app.resources import configuration
from app.resources import auth
from app.resources import turns
from app.helpers.turn import all_turns
from app.resources import helpcenter
from app.resources import user
from flask_cors import CORS, cross_origin
from datetime import date
from os import path, environ
from flask import Flask, render_template, g, current_app
from flask_session import Session
from flask_restful import Api
from config import config
from app import db
from app.db import connection
from app.models.configuration import Configuration

from datetime import date

#from app.resources.api import issue as api_issue
from app.resources import user
from app.resources import helpcenter
from app.resources import turns
from app.resources import auth
from app.resources import configuration
from app.resources import errorMessage
from app.resources import home
from app.resources.api.apicenterindex import Api_center_index
from app.resources.api.apicenter import Api_center
from app.resources.api.apiturnindex import Api_turn_index
from app.resources.api.apipostturn import Api_post_turn
#from app.resources.api import issue as api_issue

#Oauth
from authlib.integrations.flask_client import OAuth

oauth=None
def create_app(environment="development"):
    global oauth 
    # Configuración inicial de la app
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+app.config["DB_USER"] + \
        ':'+app.config["DB_PASS"]+'@' + \
        app.config["DB_HOST"]+'/'+app.config["DB_NAME"]
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_db(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)
    app.jinja_env.globals.update(has_permission=helper_permission.check)

    #Archivos
    UPLOAD_FOLDER = '/static/uploads'
    ALLOWED_EXTENSIONS = {'pdf'}


    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    #Oauth login

    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id='',
        client_secret='',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )
    facebook = oauth.register(
        name='facebook',
        client_id='',
        client_secret='',
        access_token_url='https://graph.facebook.com/v7.0/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/v7.0/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/v7.0/',
        userinfo_endpoint='https://graph.facebook.com/me?',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email '},
    )
    # API
    api = Api(app)

    # RUTAS
    # Home
    app.add_url_rule("/", "home", home.home)
    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    app.add_url_rule("/iniciar_sesion_google", "oauth_google_login", auth.OAuth_google_login)
    app.add_url_rule("/autenticacion_google", "oauth_google_authenticate", auth.OAuth_google_autorize)
    app.add_url_rule("/iniciar_sesion_facebook", "oauth_facebook_login", auth.OAuth_facebook_login)
    app.add_url_rule("/autenticacion_facebook", "oauth_facebook_authenticate", auth.OAuth_facebook_autorize)


    app.add_url_rule("/link_google", "oauth_google_link", auth.OAuth_google_link)
    app.add_url_rule("/del_link_google", "oauth_google_del_link", auth.OAuth_google_delete_Link)
    app.add_url_rule("/save_link_google", "oauth_google_savelink", auth.OAuth_google_saveLink)

    app.add_url_rule("/link_facebook", "oauth_facebook_link", auth.OAuth_facebook_link)
    app.add_url_rule("/del_link_facebook", "oauth_facebook_del_link", auth.OAuth_facebook_delete_Link)
    app.add_url_rule("/save_link_facebook", "oauth_facebook_savelink", auth.OAuth_facebook_saveLink)

    # Ruta de Configuracion
    app.add_url_rule("/configuration", "configuration_config",
                     configuration.config)
    app.add_url_rule("/configuration", "configuration_post",
                     configuration.add, methods=["POST"])

    # Mensajes de error
    app.add_url_rule("/maintenance", "error_message_maintenance",
                     errorMessage.pageUnderMaintenace)

    # Rutas de Usuarios
    app.add_url_rule("/usuarios", "user_index", user.index)
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/activate/<int:user_id>",
                     "activate_user", user.activate)
    app.add_url_rule("/usuarios/deactivate/<int:user_id>",
                     "deactivate_user", user.deactivate)
    app.add_url_rule("/usuarios/delete/<int:user_id>",
                     "delete_user", user.delete)
    app.add_url_rule("/user/edit/<username>", "edit_user", user.edit)
    app.add_url_rule("/user/edit", "post_edit",
                     user.post_edit, methods=["POST"])
    app.add_url_rule("/usuarios/profile", "user_profile", user.profile)

    # Rutas de Centros
    app.add_url_rule("/todosLosCentros", "helpcenter_index", helpcenter.index)
    app.add_url_rule("/todosLosCentros/nuevo",
                     "helpcenter_new", helpcenter.new)
    app.add_url_rule("/todosLosCentros/nuevo", "helpcenter_create",
                     helpcenter.create, methods=["POST"])
    app.add_url_rule("/todosLosCentros/accept/<int:helpcenter_id>",
                     "helpcenter_accept", helpcenter.accept)
    app.add_url_rule("/todosLosCentros/reject/<int:helpcenter_id>",
                     "helpcenter_reject", helpcenter.reject)
    app.add_url_rule("/todosLosCentros/publish/<int:helpcenter_id>",
                     "helpcenter_publish", helpcenter.publish)
    app.add_url_rule("/todosLosCentros/unpublish/<int:helpcenter_id>",
                     "helpcenter_unpublish", helpcenter.unpublish)
    app.add_url_rule("/todosLosCentros/delete/<int:helpcenter_id>",
                     "helpcenter_delete", helpcenter.delete)
    app.add_url_rule("/centro/edit/<int:helpcenter_id>",
                     "helpcenter_edit", helpcenter.edit)
    app.add_url_rule("/centro/edit", "helpcenter_post_edit",
                     helpcenter.post_edit, methods=["POST"])
    app.add_url_rule("/todosLosCentros/download/<int:helpcenter_id>",
                     "helpcenter_downloadpdf", helpcenter.download_pdf)
    api.add_resource(Api_center_index, "/centros")
    api.add_resource(Api_center, "/centros/<int:centerid>")

    # Rutas de Turnos
    app.add_url_rule("/turnos/<int:centro>/turnos_disponibles/<int:date>",
                     "turns_indexApi", turns.indexApi)
    app.add_url_rule("/turnos/<int:centro>/turnos_disponibles",
                     "turns_indexToday", turns.indexTodayApi)
    app.add_url_rule("/turnos/<int:centro>/index", "turns_index", turns.index)
    app.add_url_rule("/turnos/new/<int:helpcenter_id>", "turns_new", turns.new)
    app.add_url_rule("/turnos/new/<int:helpcenter_id>",
                     "turns_new", turns.new, methods=["POST"])
    app.add_url_rule("/turnos/edit/<int:turn_id>", "turns_edit", turns.edit)
    app.add_url_rule("/turnos/edit/<int:turn_id>",
                     "turns_edit", turns.edit, methods=["POST"])
    app.add_url_rule("/turnos/delete/<int:turn_id>",
                     "turns_delete", turns.delete)
    api.add_resource(
        Api_turn_index, "/centros/<int:idcentro>/turnos_disponibles/")
    api.add_resource(Api_post_turn, "/centros/<int:idcentro>/reserva")
    app.add_url_rule("/turnos/disponibles/<int:helpcenter_id>/<int:date>",
                     "turnos_disponibles", all_turns)

    # Estadisticas

    app.add_url_rule("/estadisticas/turnos_por_centros",
                     "estadisticas_turnos_por_centros", turns.api_centro_turnos)
    app.add_url_rule("/estadisticas/turnos_por_fechas",
                     "estadisticas_turnos_por_fechas", turns.api_fechas_turnos)

    # Ruta para el Home (usando decorator)
    # @app.route("/")
    # def home():
    #    return render_template("home.html", config=Configuration.last())

    # Rutas de API-rest
    #app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Retornar la instancia de app configurada

  
    return app
