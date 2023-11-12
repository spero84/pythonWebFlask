from homework.extensions import api
from flask_restx import fields


create_model = api.model('Create', {
    'name': fields.String(required=True, description='The item name'),
    'content': fields.String(required=True, description='The item content'),
})


read_model = api.model('Read', {
    'id': fields.Integer(required=True, description='The item identifier'),
    'name': fields.String(required=True, description='The item name'),
    'created': fields.DateTime(required=True, description='The item created datetime'),
    'content': fields.String(required=True, description='The item content'),
})

update_model = api.model('Update', {
    'id': fields.Integer(required=True, description='The item identifier'),
    'name': fields.String(required=True, description='The item name'),
    'content': fields.String(required=True, description='The item content'),
})


delete_model = api.model('Delete', {
    'id': fields.Integer(required=True, description='The item identifier'),
})


