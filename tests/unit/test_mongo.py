from unittest.mock import MagicMock

from app.mongo import get_users, create_user
from tests.fixtures import test_user, test_user_mongo, mock_db


def test_get_users_returns_empty_list(mock_db):
    """
    test that get_users returns an empty list when no users are found
    """
    mock_db.find.return_value = []
    assert [] == get_users()


def test_get_users_returns_populated_list(mock_db, test_user, test_user_mongo):
    """
    test that get_users returns a populated list,
    and that the returned records are of type User
    """
    expected = [test_user]
    mock_db.find.return_value = [test_user_mongo()]
    assert expected == get_users()


def test_create_user_returns_user(mock_db, test_user):
    """
    test that get_users returns a user after creation
    """
    mock_db.insert_one.return_value = MagicMock(inserted_id=test_user.user_id)
    assert test_user == create_user(test_user.name, test_user.email)
