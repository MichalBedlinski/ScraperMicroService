"""
    This file defines command line commands for manage.py
"""
import os
import logging

from flask import current_app
from flask_script import Command

from app.models.py_task import PyTask
from app import db


class InitDbCommand(Command):
    """ 
        Initialize the database.
        Create result directories.
    """
    def run(self):
        from app.models.py_task import PyTask
        init_db()
        logging.info('Database has been initialized.')
        make_dirs()
        logging.info('Directories created.')


def init_db():
    """
        Initialize the database.
    """
    db.drop_all()
    db.create_all()


def make_dirs():
    """
        Creates directories for results
    """
    os.makedirs(os.path.join(os.getcwd(), 'images'), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(), 'texts'), exist_ok=True)
