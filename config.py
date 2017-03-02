import os

POSTGRESQL_AUTH_URI_TEMPLATE = \
    'postgresql://{username}:{password}@{host}:{port}/{database}'


class Config:
    """
    For this application I've been running Postgres service via docker
    https://hub.docker.com/_/postgres/
    """
    SECRET_KEY = 'really not very secret key'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL_AUTH_URI_TEMPLATE.format(
        username='buddha',
        password='buddha',
        host='localhost',
        port=32768,
        database='buddha',
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
