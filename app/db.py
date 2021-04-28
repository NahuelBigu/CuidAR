import pymysql

from flask import current_app
from flask import g
from flask import cli
#SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()


def connection():
    return db


def close(e=None):
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()




"""
def init_app(app):
    global db
    conf = current_app.config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/'+conf["DB_NAME"] 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.create_all()
    #app.teardown_appcontext(close)
"""