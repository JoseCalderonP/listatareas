from flask import Flask
from decouple import config
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='mikey',
        FLASK_DATABASE_HOST = config('DATABASE_HOST'),
        FLASK_DATABASE_USER = config('DATABASE_USER'),
        FLASK_DATABASE_PASSWORD = config('DATABASE_PASSWORD'),
        FLASK_DATABASE = config('DATABASE')
    )

    from . import db 

    db.init_app(app)

    from . import auth
    from . import todo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    return app