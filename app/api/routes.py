from fastapi import APIRouter

from app.models import User, CreateUserRequest
from app import mongo

router = APIRouter()


@router.get("/users")
async def get_users() -> list[User]:
    users = mongo.get_users()
    return users


@router.post("/users")
async def create_user(user: CreateUserRequest) -> User:
    user = mongo.create_user(user.name, user.email)
    return user


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    user = mongo.get_user_by_id(user_id)
    return user
