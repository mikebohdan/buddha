from flask import Flask
from flask_admin import Admin
from flask_httpauth import HTTPTokenAuth
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin_plug = Admin()
auth = HTTPTokenAuth('Buddha-User')
auth_manager = HTTPTokenAuth('Buddha-Manager')

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# init all modules after all bateries created
import buddha.authentication
import buddha.models
import buddha.admin
import buddha.views as views


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

    # Mail configuration
    mail.init_app(app)

    # Classy registering in app
    for view in views.__all__:
        view.register(app)

    return app
