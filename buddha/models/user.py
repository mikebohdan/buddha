from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper
from sqlalchemy.orm.attributes import get_history

from buddha import db
from buddha.lib import generate_users_token
from buddha.lib import listen_for


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    passport_number = db.Column(db.String(32), nullable=False, unique=True)
    token = db.Column(db.String(1024))
    is_manager = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    #relations
    balances = db.relationship('Balance', cascade='delete')


# model actions on events

@listen_for(User, 'before_insert')
def before_add_user(
        mapper: Mapper,
        connection: Connection,
        target: User,
) -> None:
    target.token = generate_users_token(
        user_name=f'{target.first_name} {target.last_name}',
        user_passport_id=target.passport_number,
    )


@listen_for(User, 'after_update')
def after_user_acivated(
        mapper: Mapper,
        connection: Connection,
        target: User,
) -> None:
    from buddha.email import send_mail_account_created_to_user

    history = get_history(target, 'is_active')
    old_value = history.deleted[0] if history.deleted else None
    new_value = history.added[0] if history.added else None
    if new_value and not old_value:
        # In real world app there mustn't be direct call of send_mail function.
        # It's better to add celery task to queue and than process it async
        # without need of stopping whole service.
        send_mail_account_created_to_user(target)


@listen_for(User, 'before_update')
def before_user_disacivated(
        mapper: Mapper,
        connection: Connection,
        target: User,
) -> None:
    history = get_history(target, 'is_active')
    old_value = history.deleted[0] if history.deleted else None
    new_value = history.added[0] if history.added else None
    if not new_value and old_value:
        target.is_deleted = True
