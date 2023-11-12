import pytest
from homework import create_app
from homework.extensions import db
from homework.models.models import Item
from datetime import datetime


@pytest.fixture(scope='module')
def app():
    app, celery = create_app('test')

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def init_database(app):
    with app.app_context():
        db.session.add(Item(name='Test 1', content=b'content111111111', created=datetime.now()))
        db.session.add(Item(name='Test 2', content=b'content22222222222', created=datetime.now()))
        db.session.commit()

    yield db  # 테스트

    with app.app_context():
        db.session.remove()
        db.drop_all()
