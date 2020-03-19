#!/bin/bash

# Create directories
python manage.py make_dirs

# Migrate Database
./wait-for-it/wait-for-it.sh mysql:3306 -- python manage.py init_db

# Run server
python manage.py runserver --host 0.0.0.0
