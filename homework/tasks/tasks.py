from flask import current_app
from homework.models.models import Item
from homework import db
from celery import shared_task
from celery.contrib.abortable import AbortableTask
from time import sleep
from datetime import datetime


@shared_task(bind=True, base=AbortableTask)
def create_item_task(self, name, content):
    with current_app.app_context():
        item = Item(created=datetime.now(), name=name, content=content)
        db.session.add(item)
        db.session.commit()
        for i in range(10):
            print(i)
            sleep(1)
            if self.is_aborted():
                return 'TASK STOPPED!'
        return {'status': 'Item created'}


