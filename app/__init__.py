import os
from flask import Flask

if not os.getenv('SERVE_PORT'):
    print('You should set SERVE_PORT env var')
    exit(1)

if not os.getenv('SECRET_KEY'):
    print('You should generate SECRET_KEY env var')
    exit(1)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        JSONIFY_PRETTYPRINT_REGULAR=True
    )

    if test_config is None:
    # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import configs
    app.register_blueprint(configs.bp)

    from . import search
    app.register_blueprint(search.bp)

    return app
