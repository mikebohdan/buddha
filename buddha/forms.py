from wtforms import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import Length


class UserRegistrationForm(Form):
    class Meta:
        csrf = False

    first_name = StringField(
        'first_name',
        [Length(1, 32), DataRequired()],
    )
    last_name = StringField(
        'last_name',
        [Length(1, 32), DataRequired()],
    )
    email = StringField(
        'email',
        [Length(3, 128), DataRequired(), Email()],
    )
    passport_number = StringField(
        'passport_number',
        [Length(1, 32), DataRequired()],
    )
