from bson.objectid import ObjectId
from unittest.mock import MagicMock
import pytest

from app.models import User


test_user_id = '67df0469e192859207eb753a'


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
            'email': 'testuser@roryl23.ddns.net',
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
        email='testuser@roryl23.ddns.net',
    )


@pytest.fixture
def test_user_json():
    """
    Fixture to return a test user as a JSON object.
    """
    return {
        'user_id': test_user_id,
        'name': 'test user',
        'email': 'testuser@roryl23.ddns.net',
    }
