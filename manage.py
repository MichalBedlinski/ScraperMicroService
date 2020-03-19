"""
    This file sets up a command line manager.
"""
from flask_script import Manager

from app import create_app
from app.commands import InitDbCommand


manager = Manager(create_app)
manager.add_command('init_db', InitDbCommand)
manager.add_command('make_dirs', InitDbCommand)


if __name__ == "__main__":
    manager.run()
