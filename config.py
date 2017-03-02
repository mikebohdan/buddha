import os

POSTGRESQL_AUTH_URI_TEMPLATE = \
    'postgresql://{username}:{password}@{host}:{port}/{database}'


class Config:
    SECRET_KEY = 'really not very secret key'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_AUTH_URI_TEMPLATE.format(
        username='buddah',
        password='buddah',
        host='localhost',
        port=32768,
        database='buddah',
    )
    SECRET_SALT = 'my_very_secret_token_salt'
    # email config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
