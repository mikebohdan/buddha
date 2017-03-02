from json import loads as json_loads

from flask import abort
from flask import g
from flask import Blueprint
from flask import request
from flask.json import jsonify
from flask_classy import FlaskView
from flask_classy import route
from sqlalchemy.exc import IntegrityError

from buddha import auth
from buddha import auth_manager
from buddha import db
from buddha.lib import generate_users_token
from buddha.models import Balance
from buddha.models import User
from buddha.forms import UserRegistrationForm


class UserView(FlaskView):
    route_prefix = 'api'

    def post(self):
        form = UserRegistrationForm(request.form)
        if not form.validate():
            return abort(400, 'Wrong data')
        first_name = form.data.get('first_name')
        last_name = form.data.get('last_name')
        user_passport_id = form.data.get('passport_number')
        user = User(
            **form.data
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(400)
        return jsonify({'result': 'success'})

    @auth.login_required
    def get(self):
        balances = (
            db.session.query(Balance.amount, Balance.currency)
            .filter(Balance.user_id == g.user.id)
            .all()
        )

        return jsonify({
            'result': [
                balance._asdict()
                for balance in balances
            ],
        })

    @auth.login_required
    def delete(self):
        user = g.user
        try:
            user.is_active = False
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(400)
        return jsonify({'result': 'success'})


class PendingUsersView(FlaskView):
    route_prefix = 'api/manager'

    @auth_manager.login_required
    def before_request(self, name, *args, **kwargs):
        pass

    def get(self):
        users = (
            db.session.query(
                User.id,
                User.first_name,
                User.last_name,
                User.passport_number,
                User.email,
            )
            .filter(User.is_active == False)
            .filter(User.is_deleted == False)
            .filter(User.is_manager == False)
            .all()
        )
        return jsonify({
            'result': [
                dict(zip(user.keys(), user))
                for user in users
                ]
        })

    def post(self):
        user_id = request.json.get('user_id')
        if not user_id:
            return abort(400)
        user = (
            db.session.query(User)
            .filter(User.id == user_id)
            .filter(User.is_manager == False)
            .filter(User.is_deleted == False)
            .filter(User.is_active == False)
            .first()
        )
        if not user:
            return abort(404)
        try:
            user.is_active = True
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(500)
        return jsonify({'result': 'success'})



class ClosedAccountsView(FlaskView):
    route_prefix = 'api/manager'

    @auth_manager.login_required
    def before_request(self, name, *args, **kwargs):
        pass

    def get(self):
        closed_accounts = (
            db.session.query(
                User.id,
                User.first_name,
                User.last_name,
                User.passport_number,
                User.email,
            )
            .filter(User.is_deleted == True)
            .filter(User.is_manager == False)
            .all()
        )
        return jsonify({
            'results': [
                dict(zip(user.keys(), user))
                for user in closed_accounts
                ]
        })

    def delete(self):
        user_id = request.json.get('user_id')
        if not user_id:
            return abort(400)
        user = (
            db.session.query(User)
            .filter(User.id == user_id)
            .filter(User.is_active == False)
            .filter(User.is_manager == False)
            .filter(User.is_deleted == True)
            .first()
        )
        if not user:
            return abort(404)
        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return abort(500)
        return jsonify({'result': 'success'})


__all__ = [
    UserView,
    PendingUsersView,
    ClosedAccountsView,
]
