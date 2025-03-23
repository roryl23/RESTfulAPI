from bson.objectid import ObjectId
from unittest.mock import MagicMock
import pytest

from app.models import User, Post

test_user_id = '67df0469e192859207eb753a'
test_post_id = '67df0469e192859207eb753b'


@pytest.fixture
def mock_db(monkeypatch):
    """
    Fixture to patch the MongoClient in app.mongo with the mocked client.
    """
    db_mock = MagicMock(
        find=MagicMock(),
        find_one=MagicMock(),
        find_one_and_update=MagicMock(),
        delete_one=MagicMock(),
    )
    db_mock.__getitem__ = MagicMock(return_value=db_mock)

    monkeypatch.setattr('app.mongo.db', db_mock)

    return db_mock


@pytest.fixture
def test_user_mongo():
    """
    Fixture to return a test user as a dict,
    simulating a MongoDB document.
    """
    return MagicMock(
        inserted_id=ObjectId(test_user_id),
        return_value={
            '_id': ObjectId(test_user_id),
            'name': 'test user',
            'email': 'testuser@test.net',
            'version': 1,
        }
    )


@pytest.fixture
def test_user():
    """
    Fixture to return a test user as a User model instance.
    """
    return User(
        user_id=test_user_id,
        name='test user',
        email='testuser@test.net',
    )


@pytest.fixture
def test_user_json():
    """
    Fixture to return a test user as a JSON object.
    """
    return {
        'user_id': test_user_id,
        'name': 'test user',
        'email': 'testuser@test.net',
    }


@pytest.fixture
def test_user_request_json():
    """
    Fixture to return a test user request as a JSON object.
    """
    return {
        'name': 'test user',
        'email': 'testuser@test.net',
    }


@pytest.fixture
def test_post_mongo():
    """
    Fixture to return a test post as a dict,
    simulating a MongoDB document.
    """
    return MagicMock(
        inserted_id=ObjectId(test_post_id),
        return_value={
            '_id': ObjectId(test_post_id),
            'title': 'test title',
            'content': 'test content',
            'user_id': ObjectId(test_user_id),
            'version': 1,
        }
    )


@pytest.fixture
def test_post():
    """
    Fixture to return a test post as a Post model instance.
    """
    return Post(
        post_id=test_post_id,
        title='test title',
        content='test content',
        user_id=test_user_id,
    )


@pytest.fixture
def test_post_json():
    """
    Fixture to return a test post as a JSON object.
    """
    return {
        'post_id': test_post_id,
        'title': 'test title',
        'content': 'test content',
        'user_id': test_user_id,
    }


@pytest.fixture
def test_post_request_json():
    """
    Fixture to return a test post request as a JSON object.
    """
    return {
        'title': 'test title',
        'content': 'test content',
        'user_id': test_user_id,
    }
