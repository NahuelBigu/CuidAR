from flask import redirect, render_template, request, url_for, abort, session, flash
from app.models.configuration import Configuration 

def pageUnderMaintenace():
    return render_template('errorMessage/pageInMaintenance.html', config=Configuration.last())