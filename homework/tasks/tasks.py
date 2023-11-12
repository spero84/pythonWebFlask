from homework.models import Item
from homework import db
from celery import Celery
from config import config

celery = Celery(__name__)
celery.conf.broker_url = config.CELERY_BROKER_URL
celery.conf.result_backend = config.CELERY_RESULT_BACKEND


@celery.task(name="create_item_task")
def create_item_task(name, content):
    item = Item(name=name, content=content)
    db.session.add(item)
    db.session.commit()
    return {'status': 'Item created'}









