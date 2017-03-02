from sqlalchemy import ForeignKey
from sqlalchemy.types import Enum

from buddha import db

CURRENCIES = (
    'USD',
    'UAH',
    'EUR',
)


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float)
    currency = db.Column(Enum(*CURRENCIES, name='currencies'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
