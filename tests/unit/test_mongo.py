from unittest.mock import MagicMock

from pymongo.errors import OperationFailure

from app.mongo import create_record, update_record, delete_record, get_users, get_user_by_id
from tests.fixtures import test_user_id, test_user, test_user_mongo, mock_db


def test_create_record_returns_result(mock_db, test_user, test_user_mongo):
    """
    test that create_record returns a user after creation
    """
    mock_db.insert_one.return_value = test_user_mongo()
    assert test_user_mongo() == create_record(
        'users',
        {
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_create_record_handles_operationfailure_returns_false(mock_db, test_user, test_user_mongo):
    """
    test that create_record handles OperationFailure
    """
    mock_db.insert_one.side_effect = OperationFailure('fake')
    assert False == create_record(
        'users',
        {
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_create_record_handles_bad_result_returns_false(mock_db, test_user, test_user_mongo):
    """
    test that create_record handles bad result
    """
    mock_db.insert_one.return_value = None
    assert False == create_record(
        'users',
        {
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_update_record_returns_result(mock_db, test_user, test_user_mongo):
    """
    test that update_record returns a user after update
    """
    mock_db.find_one.return_value = test_user_mongo()

    test_user_updated = test_user
    test_user_updated.name = 'updated'
    test_user_updated.email = 'updated@test.net'

    test_user_mongo_updated = test_user_mongo()
    test_user_mongo_updated['name'] = 'updated'
    test_user_mongo_updated['email'] = 'updated@test.net'
    test_user_mongo_updated['version'] = 2
    mock_db.find_one_and_update.return_value = test_user_mongo_updated

    assert test_user_mongo_updated == update_record(
        'users',
        {
            '_id': test_user.user_id,
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_update_record_handles_missing_record_returns_none(mock_db, test_user, test_user_mongo):
    """
    test that update_record handles missing record
    """
    mock_db.find_one.return_value = None

    assert None == update_record(
        'users',
        {
            '_id': test_user.user_id,
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_update_record_handles_invalidid_returns_none(mock_db, test_user, test_user_mongo):
    """
    test that update_record handles invalid id
    """
    assert None == update_record(
        'users',
        {
            '_id': 'invalidid',
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_update_record_handles_operationfailure_returns_false(mock_db, test_user, test_user_mongo):
    """
    test that update_record handles OperationFailure
    """
    mock_db.find_one_and_update.side_effect = OperationFailure('fake')

    assert False == update_record(
        'users',
        {
            '_id': test_user.user_id,
            'name': test_user.name,
            'email': test_user.email,
        }
    )


def test_delete_record_returns_true(mock_db, test_user, test_user_mongo):
    """
    test that delete_record returns True after deletion
    """
    mock_db.delete_one.return_value = MagicMock(
        deleted_count=1,
        acknowledged=True,
    )
    assert True == delete_record('user', test_user.user_id)


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


def test_get_user_by_id_returns_false(mock_db):
    """
    test that get_user_by_id returns None when no user is found
    """
    mock_db.find_one.return_value = None
    assert False == get_user_by_id(test_user_id)


def test_get_user_by_id_returns_user(mock_db, test_user, test_user_mongo):
    """
    test that get_user_by_id returns type User
    """
    expected = test_user
    mock_db.find_one.return_value = test_user_mongo()
    assert expected == get_user_by_id(test_user_id)
