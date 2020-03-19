"""
    This file defines celery setup
"""
import logging
import sys

from celery import Celery
from celery.signals import after_setup_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

CELERY_TASK_LIST = [
    'app.tasks',
]

db_session = None
celery = None


def create_celery_app(_app=None):
    """
    Create a new Celery object and tie together 
    the Celery config to the app's config.

    Wrap all tasks in the context of the Flask application.

    :param _app: Flask app
    :return: Celery app
    """
    from app import db

    celery = Celery(_app.import_name,
                    broker=_app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(_app.config)
    always_eager = _app.config['TESTING'] or False
    celery.conf.update({'CELERY_ALWAYS_EAGER': always_eager})

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            if not celery.conf.CELERY_ALWAYS_EAGER:
                with _app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
            else:
                db.session = db_session
                return TaskBase.__call__(self, *args, **kwargs)

        def after_return(self, status, retval, task_id, args, kwargs, einfo):
            """
            After each Celery task, teardown our db session.

            FMI: https://gist.github.com/twolfson/a1b329e9353f9b575131

            Flask-SQLAlchemy uses create_scoped_session at startup which avoids any setup on a
            per-request basis. This means Celery can piggyback off of this initialization.
            """
            if _app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
                if not isinstance(retval, Exception):
                    db.session.commit()
            # If we aren't in an eager request (i.e. Flask will perform teardown), then teardown
            if not celery.conf.CELERY_ALWAYS_EAGER:
                db.session.remove()

    celery.Task = ContextTask

    return celery


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """
    Ensure that under Docker the Celery banner appears in the log output.
    Setup logging for celery

    FMI: https://www.distributedpython.com/2018/10/01/celery-docker-startup/
    """
    formatter = logging.Formatter(
        "%(levelname)-10s | %(filename)-20s | %(funcName)-15s | %(lineno)-5d | %(message)-50s\n"
    )
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
