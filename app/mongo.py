from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import OperationFailure

from app.config import settings
from app.models import User

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB]


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


def create_user(name: str, email: str) -> User | bool:
    try:
        result = db['users'].insert_one({
            'name': name,
            'email': email,
            'version': 1,
        })
        if not result:
            print(f"failed to create user: {result}")
            return False
        else:
            return User(
                user_id=str(result.inserted_id),
                name=name,
                email=email,
            )
    except OperationFailure as e:
        print(f"error: {e}")
        return False


def get_user_by_id(user_id: str) -> User | None:
    result = db['users'].find_one({'_id': ObjectId(user_id)})
    if result:
        return User(
            user_id=str(result['_id']),
            name=result['name'],
            email=result['email'],
        )
    else:
        return None


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


def delete_user(user_id: str) -> bool:
    try:
        result = db['users'].delete_one({'_id': ObjectId(user_id)})
        if result.acknowledged:
            return True
        else:
            print(f"failed to delete user: {result}")
            return False
    except OperationFailure as e:
        print(f"error: {e}")
        return False
