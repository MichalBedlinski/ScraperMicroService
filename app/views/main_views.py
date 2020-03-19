"""
    This file defines flask routes
"""
import os

from sqlalchemy.orm.exc import NoResultFound
from celery.states import SUCCESS as celerySUCCESS
from celery.backends.database.models import Task
from flask import Blueprint, jsonify, request, send_file

from app import db, tasks
from app.models.py_task import PyTask
from app.utility import TaskType


main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/images', methods=['POST'])
def images_orders():
    """
        Defines endpoint /images, which creates new task for image scraping
    """
    task_url = request.form.get('url')
    if not task_url:
        return jsonify({'Error' : 'No url data defined'}), 400

    # Base Directory path
    base_path = os.path.join(os.getcwd(), 'images/')

    # Celery task
    res = tasks.images_tasks.delay(task_url, base_path)

    # Celery task id
    task_id = str(res.id)

    # Path to folder
    path = os.path.join(base_path, task_id, 'images.zip')

    # Database object
    imageTask = PyTask(id=task_id, url=task_url, path=path, type=TaskType.IMAGE)
    db.session.add(imageTask)
    db.session.commit()

    return jsonify({"Task ID": task_id}), 202


@main_blueprint.route('/texts', methods=['POST'])
def texts_orders():
    """
        Defines endpoint /texts, which creates new task for text scraping
    """
    task_url = request.form.get('url')
    if not task_url:
        return jsonify({'Error' : 'No url data defined'}), 400

    # Base Directory path
    base_path = os.path.join(os.getcwd(), 'texts/')

    # Celery task
    res = tasks.text_tasks.delay(task_url, base_path)

    # Celery task id
    task_id = str(res.id)

    # Path to folder
    path = os.path.join(base_path, task_id, 'text.txt')

    # Database object
    textTask = PyTask(id=task_id, url=task_url, path=path, type=TaskType.TEXT)
    db.session.add(textTask)
    db.session.commit()

    return jsonify({"Task ID": task_id}), 202


@main_blueprint.route('/statuses/<id>', methods=['GET'])
def statuses(id):
    """
        Defines endpoint /statuses/<id>, which checks state of task
    """
    try:
        res = db.session.query(Task).filter(Task.task_id == id).one()
    except NoResultFound:
        return jsonify({'Error' : 'Task with this id does not exists'}), 404

    return jsonify({f"Task Status" : res.status}), 200


@main_blueprint.route('/images/<id>', methods=['GET'])
def images_results(id):
    """
        Defines endpoint /images/<id>, 
        which downloads result file from done task
    """
    try:
        pyTask = db.session.query(PyTask).filter(PyTask.id == id).one()
        celerTask = db.session.query(Task).filter(Task.task_id == id).one()

        if celerTask.status != celerySUCCESS:
            return jsonify(
                {'Error' : f'Task not available, current state: {celerTask.status}'}
            ), 409
    
        return send_file(
            pyTask.path, mimetype='application/zip', 
            as_attachment=True, attachment_filename='image.zip'
        )

    except NoResultFound:
        return jsonify({'Error' : 'Task with this id does not exists'}), 404


@main_blueprint.route('/texts/<id>', methods=['GET'])
def texts_results(id):
    """
        Defines endpoint /texts/<id>,
        which downloads result file from done task
    """
    try:
        pyTask = db.session.query(PyTask).filter(PyTask.id == id).one()
        celerTask = db.session.query(Task).filter(Task.task_id == id).one()
        
        if celerTask.status != celerySUCCESS:
            return jsonify(
                {'Error' : f'Task not available, current state: {celerTask.status}'}
            ), 409
    
        return send_file(
            pyTask.path, mimetype='text/plain',
            as_attachment=True, attachment_filename='text.txt'
        )

    except NoResultFound:
        return jsonify({'Error' : 'Task with this id does not exists'}), 404
