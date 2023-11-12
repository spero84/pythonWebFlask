from flask import current_app, Blueprint, request, jsonify, redirect, url_for
from homework.models.models import Item
from homework import db
from datetime import datetime
from homework import cache
from celery.result import AsyncResult
from homework.tasks.tasks import create_item_task

bp = Blueprint('main', __name__, url_prefix='/')


# @bp.route('/')
# def default_page():
#     return 'Hello World!'

# @bp.route('/create', methods=['POST'])
# def create_item():
#     req = request.get_json()
#     current_app.logger.info(req.get('name'))
#     current_app.logger.info(req.get('content'))
#     task = create_item_task.delay(req.get('name'), req.get('content'))
#     return jsonify({'task_id': task.id}), 202
#
#
# @bp.route('/create/<task_id>', methods=['GET'])
# def get_create_item_status(task_id):
#     task_result = AsyncResult(task_id)
#     result = {
#         "task_id": task_id,
#         "task_status": task_result.status,
#         "task_result": task_result.result
#     }
#     return jsonify(result), 200


@bp.route('/create', methods=['POST'])
def create_item():
    req = request.get_json()
    content = req.get('content')
    current_app.logger.info(req.get('name'))
    current_app.logger.info(req.get('content'))
    item = Item(created=datetime.now(), name=req.get('name'), content=req.get('content'))
    db.session.add(item)
    try:
        db.session.commit()
        return jsonify(item.serialize()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 500


@bp.route('/read/<int:id>', methods=['GET'])
@cache.cached(timeout=120)
def read_item(id):
    item = Item.query.get_or_404(id)
    return item.serialize()


@bp.route('/update/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    req = request.get_json()
    item.name = req.get('name')
    item.content = req.get('content')
    try:
        db.session.commit()
        return jsonify(item.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        return jsonify(), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


