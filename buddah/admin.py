from flask_admin.contrib.sqla import ModelView

from buddah import admin_plug as admin
from buddah import db
from buddah.models import User


class AdminModelView(ModelView):
    can_create = True
    can_delete = True
    can_delete = True
    can_view_details = True

    column_exclude_list = [
        'token',
        'balances',
    ]

    form_excluded_columns = [
        'token',
        'balances',
        'is_deleted',
    ]

admin.add_view(AdminModelView(User, db.session))
