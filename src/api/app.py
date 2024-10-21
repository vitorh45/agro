import logging
import sys
from os import getenv

import json_logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


load_dotenv()

ENV = getenv("DEPLOY_ENV", default="Development")

convention = {
    "ix": "ix_%(column_0_label)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
    "uq": "%(table_name)s_%(column_0_name)s_key"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata) 

def create_app(deploy_env: str = ENV) -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f"api.config.{deploy_env}Config")

    __configure_logger(app=app)
    __register_blueprints(app=app)

    db.init_app(app)
    Migrate(app, db)

    return app


def __configure_logger(app: Flask) -> None:
    if not json_logging.ENABLE_JSON_LOGGING:
        json_logging.init_flask(enable_json=True)
        json_logging.init_request_instrument(app=app)

    logger = logging.getLogger("agro")
    logger.setLevel(app.config["LOGS_LEVEL"])

    if not logger.hasHandlers():
        logger.addHandler(logging.StreamHandler(sys.stdout))


def __register_blueprints(app: Flask) -> None:
    from api.views import (
        bp_index,
        bp_farmer
    )
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_farmer)
