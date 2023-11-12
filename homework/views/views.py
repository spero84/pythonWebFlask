from flask import current_app, Blueprint, request, jsonify, send_file
from homework.models.models import Item
from homework import db
from datetime import datetime
from homework import cache
import base64
import json
import io


bp = Blueprint('main', __name__, url_prefix='/')



# @bp.route('/create', methods=['POST'])
# def create_item():
#     name = request.form['name']
#     file = request.files['content']
#     content = file.read() if file else None
#     task = create_item_task.delay(name=name, content=content)
#     return jsonify({'message': 'Task created', 'task_id': task.id}), 202
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
    name = request.form['name']
    file = request.files['content']
    content = file.read() if file else None
    current_app.logger.debug(content)
    item = Item(created=datetime.now(), name=name, content=content)
    db.session.add(item)
    try:
        db.session.commit()
        string_data = content.decode('utf-8')
        return jsonify({"message": "Data created", "id": item.id, "content": string_data,
                        "created": item.created}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 500



# @bp.route('/create', methods=['POST'])
# def create_item():
#     req = request.get_json()
#     content = req.get('content')
#     current_app.logger.info(req.get('name'))
#     current_app.logger.info(req.get('content'))
#     item = Item(created=datetime.now(), name=req.get('name'), content=req.get('content'))
#     db.session.add(item)
#     try:
#         db.session.commit()
#         return jsonify(item.serialize()), 201
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.info(str(e))
#         return jsonify({'error': str(e)}), 500


@bp.route('/read/<int:id>', methods=['GET'])
@cache.cached(timeout=120)
def read_item(id):
    item = Item.query.get_or_404(id)
    byte_data = item.content
    current_app.logger.debug(byte_data)
    string_data = byte_data.decode('utf-8')
    # if byte_data:
    #     byte_data =base64.b64encode(byte_data).decode('utf-8')
    return jsonify({"id": item.id, "name": item.name,
                    "content": string_data, "created": item.created})


# @bp.route('/read/<int:id>', methods=['GET'])
# @cache.cached(timeout=120)
# def read_item(id):
#     item = Item.query.get_or_404(id)
#     return item.serialize()


@bp.route('/update/', methods=['PUT'])
def update_item():
    id = request.form['id']
    name = request.form['name']
    file = request.files['content']
    content = file.read() if file else None
    current_app.logger.debug(content)
    item = Item.query.get_or_404(id)
    item.id = id
    item.name = name
    item.content = content
    try:
        db.session.commit()
        string_data = content.decode('utf-8')
        return jsonify({"message": "Data updated", "name": item.name, "id": item.id, "content": string_data,
                        "created": item.created}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# @bp.route('/update/<int:id>', methods=['PUT'])
# def update_item(id):
#     item = Item.query.get_or_404(id)
#     req = request.get_json()
#     item.name = req.get('name')
#     item.content = req.get('content')
#     try:
#         db.session.commit()
#         return jsonify(item.serialize()), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500
#

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        return jsonify({"message": "Item deleted", "id": id}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


