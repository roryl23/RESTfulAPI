from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from pymongo.errors import OperationFailure

from app.main import app
from tests.fixtures import (
    test_user_json,
    test_user_request_json,
    mock_db,
    test_user_mongo,
    test_post_json,
    test_post_request_json,
    test_post_mongo
)

client = TestClient(app)


def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the RESTfulAPI!'}


def test_get_users_success(mock_db, test_user_mongo, test_user_json):
    mock_db.find.return_value = [test_user_mongo()]
    response = client.get(f"/users")
    assert response.status_code == 200
    assert response.json() == [test_user_json]


def test_get_users_failure(mock_db):
    mock_db.find.return_value = []
    response = client.get(f"/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user_success(mock_db, test_user_mongo, test_user_json):
    mock_db.insert_one.inserted_id = test_user_mongo.inserted_id
    mock_db.insert_one.return_value = test_user_mongo
    mock_db.find_one.return_value = test_user_mongo()
    response = client.post('/users', json=test_user_json)
    assert response.status_code == 201
    assert response.json() == test_user_json


def test_create_user_failure(mock_db, test_user_json):
    mock_db.insert_one.side_effect = OperationFailure('fake')
    response = client.post('/users', json=test_user_json)
    assert response.status_code == 500


def test_create_user_handles_missing_user(mock_db, test_user_mongo, test_user_json):
    mock_db.insert_one.inserted_id = test_user_mongo.inserted_id
    mock_db.insert_one.return_value = test_user_mongo
    mock_db.find_one.return_value = None
    response = client.post('/users', json=test_user_json)
    assert response.status_code == 404


def test_get_user_by_id_success(mock_db, test_user_mongo, test_user_json):
    mock_db.find_one.return_value = test_user_mongo()
    response = client.get(f"/users/{test_user_json['user_id']}")
    assert response.status_code == 200
    assert response.json() == test_user_json


def test_get_user_by_id_handles_missing_user(mock_db, test_user_json):
    mock_db.find_one.return_value = None
    response = client.get(f"/users/{test_user_json['user_id']}")
    assert response.status_code == 404


def test_update_user_success(mock_db, test_user_mongo, test_user_json, test_user_request_json):
    mock_db.find_one_and_update.return_value = test_user_mongo()
    mock_db.find_one.return_value = test_user_mongo()
    response = client.put(
        f"/users/{test_user_json['user_id']}",
        json=test_user_request_json
    )
    assert response.status_code == 200
    assert test_user_json == response.json()


def test_update_user_failure(mock_db, test_user_json, test_user_request_json):
    mock_db.find_one_and_update.side_effect = OperationFailure('fake')
    response = client.put(
        f"/users/{test_user_json['user_id']}",
        json=test_user_request_json
    )
    assert response.status_code == 500


def test_update_user_handles_updaterecord_failure(mock_db, test_user_request_json):
    response = client.put(
        f"/users/invalidid",
        json=test_user_request_json
    )
    assert response.status_code == 404


def test_update_user_handles_missing_user_failure(mock_db, test_user_mongo, test_user_json, test_user_request_json):
    mock_db.find_one_and_update.return_value = test_user_mongo()
    mock_db.find_one.return_value = None
    response = client.put(
        f"/users/{test_user_json['user_id']}",
        json=test_user_request_json
    )
    assert response.status_code == 404


def test_delete_user_success(mock_db, test_user_json):
    mock_db.delete_one.return_value = MagicMock(
        deleted_count=1,
        acknowledged=True,
    )
    response = client.delete(f"/users/{test_user_json['user_id']}")
    assert response.status_code == 204


def test_delete_user_failure(mock_db, test_user_json):
    mock_db.delete_one.return_value = MagicMock(
        deleted_count=0,
        acknowledged=True,
    )
    response = client.delete(f"/users/{test_user_json['user_id']}")
    assert response.status_code == 404


def test_get_posts_success(mock_db, test_post_mongo, test_user_mongo, test_post_json):
    mock_db.find.return_value = [test_post_mongo()]
    response = client.get(f"/posts")
    assert response.status_code == 200
    assert response.json() == [test_post_json]


def test_get_posts_failure(mock_db):
    mock_db.find.return_value = []
    response = client.get(f"/posts")
    assert response.status_code == 200
    assert response.json() == []


def test_create_post_success(mock_db, test_user_mongo, test_post_mongo, test_post_json):
    mock_db.find_one.side_effect = [test_user_mongo(), test_post_mongo()]
    mock_db.insert_one.inserted_id = test_post_mongo.inserted_id
    mock_db.insert_one.return_value = test_post_mongo
    response = client.post('/posts', json=test_post_json)
    assert response.status_code == 201
    assert response.json() == test_post_json


def test_create_post_handles_missing_user(mock_db, test_post_json):
    mock_db.find_one.return_value = None
    response = client.post('/posts', json=test_post_json)
    assert response.status_code == 400


def test_create_post_handles_missing_post(mock_db, test_user_mongo, test_post_mongo, test_post_json):
    mock_db.find_one.side_effect = [test_user_mongo(), None]
    mock_db.insert_one.inserted_id = test_post_mongo.inserted_id
    mock_db.insert_one.return_value = test_post_mongo
    mock_db.find_one.return_value = None
    response = client.post('/posts', json=test_post_json)
    assert response.status_code == 404


def test_get_post_by_id_success(mock_db, test_post_mongo, test_post_json):
    mock_db.find_one.return_value = test_post_mongo()
    response = client.get(f"/posts/{test_post_json['post_id']}")
    assert response.status_code == 200
    assert response.json() == test_post_json


def test_get_post_by_id_handles_missing_post(mock_db, test_post_json):
    mock_db.find_one.return_value = None
    response = client.get(f"/posts/{test_post_json['post_id']}")
    assert response.status_code == 404


def test_update_post_success(mock_db, test_post_mongo, test_post_json, test_post_request_json):
    mock_db.find_one.return_value = test_post_mongo()
    mock_db.find_one_and_update.return_value = test_post_mongo()
    response = client.put(
        f"/posts/{test_post_json['post_id']}",
        json=test_post_request_json
    )
    assert response.status_code == 200
    assert test_post_json == response.json()


def test_update_post_failure(mock_db, test_post_json, test_post_request_json):
    mock_db.find_one_and_update.side_effect = OperationFailure('fake')
    response = client.put(
        f"/posts/{test_post_json['post_id']}",
        json=test_post_request_json
    )
    assert response.status_code == 500


def test_update_post_handles_updaterecord_failure(mock_db, test_post_request_json):
    response = client.put(
        f"/posts/invalidid",
        json=test_post_request_json
    )
    assert response.status_code == 500


def test_update_post_handles_missing_post_failure(mock_db, test_post_mongo, test_post_json, test_post_request_json):
    mock_db.find_one.side_effect = [test_post_mongo(), None]
    mock_db.find_one_and_update.return_value = test_post_mongo()
    response = client.put(
        f"/posts/{test_post_json['post_id']}",
        json=test_post_request_json
    )
    assert response.status_code == 404


def test_delete_post_success(mock_db, test_post_json):
    mock_db.delete_one.return_value = MagicMock(
        deleted_count=1,
        acknowledged=True,
    )
    response = client.delete(f"/posts/{test_post_json['post_id']}")
    assert response.status_code == 204


def test_delete_post_failure(mock_db, test_post_json):
    mock_db.delete_one.return_value = MagicMock(
        deleted_count=0,
        acknowledged=True,
    )
    response = client.delete(f"/posts/{test_post_json['post_id']}")
    assert response.status_code == 404
