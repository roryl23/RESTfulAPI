from app.mongo import get_users, create_user, get_user_by_id, update_user
from tests.fixtures import test_user_id, test_user, test_user_mongo, mock_db


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


def test_create_user_returns_user(mock_db, test_user, test_user_mongo):
    """
    test that create_user returns a user after creation
    """
    mock_db.insert_one.return_value = test_user_mongo
    assert test_user == create_user(test_user.name, test_user.email)


def test_get_user_by_id_returns_none(mock_db):
    """
    test that get_user_by_id returns None when no user is found
    """
    mock_db.find_one.return_value = None
    assert None == get_user_by_id(test_user_id)


def test_get_user_by_id_returns_user(mock_db, test_user, test_user_mongo):
    """
    test that get_user_by_id returns type User
    """
    expected = test_user
    mock_db.find_one.return_value = test_user_mongo()
    assert expected == get_user_by_id(test_user_id)


def test_update_user_returns_user(mock_db, test_user, test_user_mongo):
    """
    test that update_user_by_id returns a user after update
    """
    mock_db.find_one.return_value = test_user_mongo()

    test_user_updated = test_user
    test_user_updated.name = 'updated'
    test_user_updated.email = 'updated@roryl23.ddns.net'

    test_user_mongo_updated = test_user_mongo()
    test_user_mongo_updated['name'] = 'updated'
    test_user_mongo_updated['email'] = 'updated@roryl23.ddns.net'
    test_user_mongo_updated['version'] = 2
    mock_db.find_one_and_update.return_value = test_user_mongo_updated

    assert test_user_updated == update_user(test_user_updated)
