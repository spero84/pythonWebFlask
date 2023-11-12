import pytest
from homework import create_app, db
from homework.models.models import Item
from datetime import datetime
from app import app as flask_app

@pytest.fixture(scope='module')
def app():
    app = create_app('test')
    # config test
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client('test')

@pytest.fixture(scope='module')
def init_database(app):
    """Initialize the database."""
    with app.app_context():
        db.session.add(Item(name='Test 1', content='content111111111', created=datetime.now()))
        db.session.add(Item(name='Test 2', content='content22222222222', created=datetime.now()))
        db.session.commit()

    yield db  # 이 위치에서 테스트가 실행됩니다.

    # 테스트 후 데이터베이스 정리
    with app.app_context():
        db.session.remove()
        db.drop_all()
