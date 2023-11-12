from flask import Blueprint
from flask_restx import Namespace, Resource
from homework.models.models import Item
from homework.models.api_models import read_model, create_model, update_model, delete_model
from datetime import datetime
from homework.extensions import db

blueprint = Blueprint('items', __name__,  url_prefix='/items')
ns = Namespace('items', description='Items operations')


@ns.route('/create')
class CreateAPI(Resource):
    @ns.expect(create_model)
    @ns.marshal_with(read_model)
    def post(self):
        print(ns.payload)
        item = Item(name=ns.payload['name'], content=ns.payload['content'].encode(), created=datetime.now())
        db.session.add(item)
        db.session.commit()
        return item, 201


@ns.route('/read/<int:id>')
class ReadAPI(Resource):
    @ns.marshal_with(read_model)
    def get(self, id):
        return Item.query.get(id)

@ns.route('/update')
class UpdateAPI(Resource):
    @ns.expect(update_model)
    @ns.marshal_with(update_model)
    def put(self):
        print(ns.payload)
        item = Item.query.get(ns.payload['id'])
        item.name = ns.payload['name']
        item.content = ns.payload['content']
        db.session.commit()
        return item


@ns.route('/delete/<int:id>')
class UpdateAPI(Resource):
    @ns.expect(delete_model)
    @ns.marshal_with(delete_model)
    def delete(self, id):
        item = Item.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return {"id": item.id}, 204
