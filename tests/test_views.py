import pytest
from homework.models.models import Item
from homework import db
from datetime import datetime
import logging


def test_create_item(init_database):
    """Test item creation."""
    item1 = Item(name='Test 10', content='content1101010101010101011111111', created=datetime.now())
    db.session.add(item1)
    db.session.commit()
    assert item1.id is not None


def test_read_item(init_database):
    """Test item reading."""
    item = Item.query.first()
    assert item is not None


def test_update_item(init_database):
    """Test item updating."""
    item = Item.query.first()
    item.name = 'Updated Name'
    db.session.commit()
    updated_item = Item.query.first()
    assert updated_item.name == 'Updated Name'

def test_delete_item(init_database):
    """Test item deletion."""
    item = Item.query.first()
    logging.debug(item)
    db.session.delete(item)
    db.session.commit()
    deleted_item = Item.query.first()
    logging.debug(deleted_item)
    assert deleted_item is not item