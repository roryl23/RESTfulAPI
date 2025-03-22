from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult

from app.config import settings
from app.models import User

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB]


def create_record(collection: str, record: dict) -> InsertOneResult | bool:
    try:
        record['version'] = 1
        result = db[collection].insert_one(record)
        if result:
            return result
        else:
            print(f"failed to create user: {result}")
            return result
    except OperationFailure as e:
        print(f"error: {e}")
        return False


def delete_record(collection:str, _id: str) -> bool:
    try:
        result = db[collection].delete_one({'_id': ObjectId(_id)})
        if result.acknowledged:
            return True
        else:
            print(f"failed to delete record: {result}")
            return False
    except OperationFailure as e:
        print(f"error: {e}")
        return False


def get_users() -> list[User]:
    results = db['users'].find()
    if results:
        users = []
        for record in results:
            users.append(User(
                user_id=str(record['_id']),
                name=record['name'],
                email=record['email'],
            ))
        return users
    else:
        return []


def get_user_by_id(user_id: str) -> User | bool:
    result = db['users'].find_one({'_id': ObjectId(user_id)})
    if result:
        return User(
            user_id=str(result['_id']),
            name=result['name'],
            email=result['email'],
        )
    else:
        return False


def update_user(user: User) -> User | bool:
    """
    Update a user in the database atomically.
    """
    try:
        current = db['users'].find_one({'_id': ObjectId(user.user_id)})
        if not current:
            return False

        result = db['users'].find_one_and_update(
            {'_id': ObjectId(user.user_id), 'version': current['version']},
            { '$set': {
                'name': user.name,
                'email': user.email,
                'version': current['version'] + 1,
            }},
            return_document=True
        )

        if result:
            return User(
                user_id=str(result['_id']),
                name=result['name'],
                email=result['email'],
            )
        else:
            print(f"update failed due to version mismatch: {result}")
            return False
    except OperationFailure as e:
        print(f"error: {e}")
        return False
