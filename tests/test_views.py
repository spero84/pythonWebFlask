import pytest
from homework.models.models import Item
import responses
import logging


def test_create_item(client, app):
    client.post("/create", data={"name": "pytest_name", "content": b"pytest contents"})
    with app.app_context():
        assert Item.query.count() == 1
        assert Item.query.first().name == "pytest_name"


def test_read_item(client):
    response = client.get("/read/1")
    assert "pytest_name" in response.data


def test_update_item(client):
    response = client.put("/update", data={"name": "pytest_update", "content": b"pytest contents"})
    assert "pytest_update" in response.data


def test_delete_item(client):
    response = client.get("/read/1")
    id = response.get_json().get('id')
    response2 = client.delete("/delete/"+id)

    assert "Item deleted" in response2.data