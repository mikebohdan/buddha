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
