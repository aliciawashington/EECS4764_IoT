import os
from datetime import datetime
from flask import Flask, render_template



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='thatscrazy',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
    )

    if test_config is None:
       app.config.from_pyfile('config.py', silent=True) 
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from application import machine
    app.register_blueprint(machine.bp)

    @app.route('/')
    def home():
        now  = datetime.now()
        timeString = now.strftime("%m/%d/%Y %H:%M:%S")

        templateData = {
            'title': 'Machine Operation Dashboard',
            'time': timeString
        }
        return render_template('index.html', **templateData)
    return app