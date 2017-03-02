from flask_mail import Message

from buddha import mail
from buddha.models import User

ACCOUNT_CREATED_MSG_TMPL = (
    "Добрый день, {user_name}. \n"
    "Ваш аккаунт успешно создан и прошел проверку у нашего менеджера. "
    "Ваш ключь для аутентефикации: {token}\n"
    "Спасибо!"
)


def send_mail_account_created_to_user(user: User) -> None:
    message = ACCOUNT_CREATED_MSG_TMPL.format(
        user_name = user.first_name,
        token=user.token,
    )
    subject = "Ваш аккаунт успешно создан!"
    msg = Message(recipients=[user.email], body=message, subject=subject)
    mail.send(msg)
