import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['FLASK_DATABASE_HOST'],
            user = current_app.config['FLASK_DATABASE_USER'],
            password = current_app.config['FLASK_DATABASE_PASSWORD'],
            database = current_app.config['FLASK_DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    
    for i in instructions:
        c.execute(i)

    db.commit()

@click.command('init-db')
@with_appcontext

def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

##Cuando termine de ejutar una peticion cierra la conexion de la base de datos
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)