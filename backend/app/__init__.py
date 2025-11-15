import os
from flask import Flask
from flask_cors import CORS

from .models import db
from .views import view
from .chinavis_data import data


DEFAULT_DB_URI = 'mysql+pymysql://chinavis:123456@127.0.0.1/chinavis'


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {'1', 'true', 't', 'yes', 'y', 'on'}


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    db_uri = os.environ.get('CHINAVIS_DB_URI', DEFAULT_DB_URI)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('FLASK_SECRET', os.urandom(64)),
        GITHUB_SECRET=os.environ.get('GITHUB_SECRET', '4Qqk3NVez2Sea603c2ZwDqPb172SqOsIsEuzMvktDTnurIBKAI1SPoW5wHMCa71e'),
        REPO_PATH=os.environ.get('REPO_PATH', '/usr/src/app'),
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=db_uri,
        DEBUG=_bool_env('FLASK_DEBUG', True)
    )

    CORS(app)
    db.init_app(app)
    app.register_blueprint(view)
    app.register_blueprint(data)

    return app
