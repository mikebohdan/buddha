from hashlib import sha3_512
from functools import wraps

from flask import current_app as app
from sqlalchemy import event


def generate_users_token(user_name: str, user_passport_id: str) -> str:
    salt = app.config['SECRET_SALT']
    hash = sha3_512(
        f'u={user_name}-id={user_passport_id}-s={salt}'
        .encode()
    )
    return hash.hexdigest()


def listen_for(model, event_name):
    def decorator(func):
        event.listen(model, event_name, func)
    return decorator
