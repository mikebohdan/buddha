from flask import Flask
from flask_admin import Admin
from flask_httpauth import HTTPTokenAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin_plug = Admin()
auth = HTTPTokenAuth('Buddah-User')
auth_manager = HTTPTokenAuth('Buddah-Manager')

db = SQLAlchemy()
migrate = Migrate()

import buddah.authentication
import buddah.models
import buddah.admin
import buddah.views as views


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Config admin part
    admin_plug.init_app(app)

    # DB config
    db.init_app(app)
    db.create_all(app=app)

    # Migrate config
    migrate.init_app(db=db, app=app)

    # Classy registering in app
    for view in views.__all__:
        view.register(app)

    return app
