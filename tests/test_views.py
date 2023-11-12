from homework.models.models import Item
from io import BytesIO

def test_create_item(client, app):
    client.post("/create",
                data={"name": "pytest_name", "content": (BytesIO(b'my file contents'), 'text.txt')},
                content_type='multipart/form-data')
    with app.app_context():
        assert Item.query.count() == 1
        assert Item.query.first().name == "pytest_name"


def test_read_item(client):
    response = client.get("/read/1")
    assert response.status_code == 200
    assert "pytest_name" == response.json.get('name')


def test_update_item(client, app):
    # with app.app_context():
    response = client.put("/update",
                          data={"id": 1, "name": "pytest_update",
                                "content": (BytesIO(b'my file contents'), 'update.txt')},
                          content_type='multipart/form-data')
    assert response.status_code == 201
    assert Item.query.get(1).name == "pytest_update"


def test_delete_item(client):
    response = client.get("/read/1")
    id = response.get_json().get('id')
    response2 = client.delete("/delete/"+str(id))



