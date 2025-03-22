from fastapi.testclient import TestClient

from app.main import app
from tests.fixtures import test_user, test_user_json, mock_db, test_user_mongo

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the RESTfulAPI!'}


def test_get_users(mock_db, test_user_mongo, test_user, test_user_json):
    mock_db.find.return_value = [test_user_mongo()]
    response = client.get(f"/users")
    assert response.status_code == 200
    assert response.json() == [test_user_json]


def test_get_user_by_id(mock_db, test_user_mongo, test_user, test_user_json):
    mock_db.find_one.return_value = test_user_mongo()
    response = client.get(f"/users/{test_user_json['user_id']}")
    assert response.status_code == 200
    assert response.json() == test_user_json


def test_create_user(mock_db, test_user_mongo, test_user_json):
    mock_db.insert_one.inserted_id = test_user_mongo.inserted_id
    mock_db.insert_one.return_value = test_user_mongo
    response = client.post('/users', json=test_user_json)
    assert response.status_code == 200
    assert response.json() == test_user_json


def test_create_user_invalid():
    invalid_data = {'description': 'Missing name'}
    response = client.post('/users', json=invalid_data)
    assert response.status_code == 422
    assert 'detail' in response.json()
