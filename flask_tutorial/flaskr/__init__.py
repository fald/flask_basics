from flask import Flask
import os

# Instead of creating the Flask instance globally at the top of a file,
# put it in a function, the 'application factory'
# Config, registration, setup, and so on, done within the app-factory function.

# This file specifically will tell Python to treat 'flaskr' as a package.

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # Should be overridden for deployment
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load instance config when not testing, if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config
        app.config.from_mapping(test_config)

    # Instance folder exists?
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Simplest page
    @app.route('/hello')
    def hello():
        return "Hello, world!"

    return app