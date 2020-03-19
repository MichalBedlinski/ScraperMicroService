"""
    Package init
"""
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instantiate Flask extensions
from app import celeryapp

db = SQLAlchemy()

# Set up Python logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)-10s | %(filename)-20s | %(funcName)-15s | %(lineno)-5d | %(message)-50s\n")


def create_app(extra_config_settings={}):
    """
        Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings
    app.config.from_object('app.settings')

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Celery
    celery = celeryapp.create_celery_app(app)
    celeryapp.celery = celery

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    return app
