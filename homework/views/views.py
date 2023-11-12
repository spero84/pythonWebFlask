from flask import Blueprint, request, jsonify, redirect, url_for
from homework.models.models import Item
from homework import db
from datetime import datetime
from homework import cache
from homework.forms.forms import DataForm
from celery.result import AsyncResult
from homework.tasks.tasks import create_item_task

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def default_page():  # put application's code here
    return 'Hello World!'


@bp.route('/create', methods=['POST'])
def create_item():
    form = DataForm()
    if form.validate_on_submit():
        byte_data = form.file.data.read() if form.file.data else None
        task = create_item_task.delay(form.name.data, byte_data)
        return jsonify({'task_id': task.id}), 202

    return jsonify('!!! something error'), 500

'''
def create_item():
    req = request.get_json()
    name = req.get_json('name')
    byte_data = request.files['content'].read()

    return jsonify({'task_id': task.id}), 202
'''

# def create_item():
#     req = request.get_json()
#     content = req.get('content')
#     current_app.logger.info(name)
#     current_app.logger.info(content)
#     item = Item(created=datetime.now(), name=req.get('name'), content=req.get('content'))
#     db.session.add(item)
#     try:
#         db.session.commit()
#         return jsonify(item.serialize()), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500



@bp.route('/create/<task_id>', methods=['GET'])
def get_create_item_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200



@bp.route('/read/<int:id>', methods=['GET'])
@cache.cached(timeout=120)
def read_item(id):
    item = Item.query.get_or_404(id)
    return item.serialize()


@bp.route('/update/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    req = request.get_json()
    content = req.get('content')
    item.modify_created = datetime.now()
    item.modify_name = req.get('name')
    item.modify_content = req.get('content')
    try:
        db.session.commit()
        return jsonify(item.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_item():
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        return jsonify(), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


