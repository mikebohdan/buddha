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
    """
    This endpoint is used for users part of API.
    With POST request you can simply create new user, but he still be need
    approvement of Manager.
    With GET requeset you can get all users balances.
    With DELETE request you can simply delete user from system, but for complex
    deletion it still need aprovement of manager.

    For accessing all methods use path "/api/user/"
    """
    route_prefix = 'api'

    def post(self):
        """
        This endpoint expects FORM in following format
            first_name: <users first name>
            last_name: <users last name>
            email: <users email>
            passport_number: <users passport number>

        If user was successfully added returns JSON with following content
        {
            "result": "success"
        }
        otherwise raises HTTP-400 Bad Request
        """
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
        """
        This method provides users ability to monitor theirs balances.
        For using it you need to specify following header in your request
            Authorization: Buddha-User <your token>
        returns: JSON with in following format
        {
            "result": [
                {
                    "amount": <float value>,
                    "currency": <current balance currency>
                },
                ...
            ]
        }
        """
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
        """
        This methods allows you to delete your account.
        As GET method this also need header
            Authorization: Buddha-User <your token>
        If your account seccessfully deleted you'll recive JSON
        {
            "result": "success"
        }
        otherwise HTTP-400 Bad request
        """
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
    """
    This endpoint collect all methods to manipulate users account that
    pending in approvment queue.

    For using this API you need to specifu following path
        "/api/manager/pendingusers/"

    For all endpoints you need to know your token that you can resive from your
    administrator.

    Also you need to specify following header for every request you make
        Authorization: Buddha-Manager <your token>
    """
    route_prefix = 'api/manager'

    @auth_manager.login_required
    def before_request(self, name, *args, **kwargs):
        pass

    def get(self):
        """
        This method provides you list of all pending users.
        Returns JSON in following format
        {
            "result": [
                {
                    "id": <users id>,
                    "first_name": <users first name>,
                    "last_name": <users last name>,
                    "passport_number": <users passport number>,
                    "email": <users email>,
                },
                ...
            ]
        }
        """
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
        """
        With this method you can approve chosen user.
        It expects JSON body in following format
        {
            "user_id": <user id>
        }
        If user was successfully approved returns JSON in following format
        {
            "result": "success"
        }
        If user_id not founded in our database - HTTP-404 Not found
        Otherwise - HTTP-400 Bad request
        """
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
            return abort(400)
        return jsonify({'result': 'success'})



class ClosedAccountsView(FlaskView):
    """
    This endpoint provides all method that you need to manipulate with accounts
    in deletion queue.

    For manipulating with this endpoint use following path
        "/api/manager/closedaccounts/"

    For all endpoints you need to know your token that you can resive from your
    administrator.

    Also you need to specify following header for every request you make
        Authorization: Buddha-Manager <your token>
    """
    route_prefix = 'api/manager'

    @auth_manager.login_required
    def before_request(self, name, *args, **kwargs):
        pass

    def get(self):
        """
        Returns deletion queue in following format
        {
            "result": [
                {
                    "id": <users id>,
                    "first_name": <users first name>,
                    "last_name": <users last name>,
                    "passport_number": <users passport number>,
                    "email": <users email>,
                },
                ...
            ]
        }
        """
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
        """
        Provides functionality for deleting chosen account.
        It expects JSON body in following format
        {
            "user_id": <user id>
        }
        If user was successfully approved returns JSON in following format
        {
            "result": "success"
        }
        If user_id not founded in our database - HTTP-404 Not found
        Otherwise - HTTP-400 Bad request
        """
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
            return abort(400)
        return jsonify({'result': 'success'})


__all__ = [
    UserView,
    PendingUsersView,
    ClosedAccountsView,
]
