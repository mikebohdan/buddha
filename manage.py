from flask_script import Manager
from flask_migrate import MigrateCommand

from buddha import create_app
from config import Config

app = create_app(Config)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    from urllib.parse import unquote
    from flask import url_for
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = unquote("{:50s} {:20s} {}"
                       .format(rule.endpoint, methods, url))
        output.append(line)
    for line in sorted(output):
        print(line)

manager.run()
