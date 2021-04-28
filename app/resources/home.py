from flask import  render_template,redirect,url_for
from app.helpers.control_decorator import control
from app.models.configuration import Configuration


def home():
    if not Configuration.last().habilitate:
        return redirect(url_for("error_message_maintenance"))
    return render_template("home.html", config=Configuration.last())