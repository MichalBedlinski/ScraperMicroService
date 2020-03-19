"""
    This file defines global settings
"""
import os

# Application settings
APP_NAME = os.environ.get("APP_NAME", "Scraper Micro Service")

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS", False)

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SQLALCHEMY_DATABASE_URI", 'mysql+pymysql://root:@127.0.0.1/db')

# Celery
CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL", 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", 'db+mysql+pymysql://root:@127.0.0.1/db')
