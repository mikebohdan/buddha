from flask import g

from buddha import auth
from buddha import auth_manager
from buddha import db
from buddha.models import User


@auth.verify_token
def verify_token(token):
    g.user = None
    user = db.session.query(User).filter(User.token == token).first()
    if not (user and user.is_active):
        return False
    g.user = user
    return True

@auth_manager.verify_token
def verify_manager_token(token):
    g.manager = None
    manager = db.session.query(User).filter(User.token == token).first()
    if not (manager and manager.is_active and manager.is_manager):
        return False
    g.manager = manager
    return True
