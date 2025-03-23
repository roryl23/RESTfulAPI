import random
import time
from typing import Mapping
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult

from app.config import settings
from app.models import User, Post

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


def update_record(collection: str, record: dict) -> Mapping | None | bool:
    """
    Update a record in the database atomically,
    with stochastic retry delays.
    """
    while True:
        try:
            _id = ObjectId(record['_id'])
            current = db[collection].find_one({'_id': _id})
            if not current:
                return None

            updates = {k: v for k, v in record.items() if k != '_id'}
            updates['version'] = current['version'] + 1
            result = db[collection].find_one_and_update(
                {'_id': _id, 'version': current['version']},
                {'$set': updates},
                return_document=True
            )
            if result:
                return result
            else:
                # stochastic delay from 0 to 5 ms
                time.sleep(random.uniform(0, 0.005))
        except InvalidId as e:
            print(f"error: {e}")
            return None
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


def get_posts() -> list[Post]:
    results = db['posts'].find()
    if results:
        posts = []
        for record in results:
            posts.append(Post(
                post_id=str(record['_id']),
                title=record['title'],
                content=record['content'],
                user_id=record['user_id'],
            ))
        return posts
    else:
        return []


def get_post_by_id(post_id: str) -> Post | bool:
    result = db['posts'].find_one({'_id': ObjectId(post_id)})
    if result:
        return Post(
            post_id=str(result['_id']),
            title=result['title'],
            content=result['content'],
            user_id=result['user_id'],
        )
    else:
        return False
