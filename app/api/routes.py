from fastapi import APIRouter

from app.models import User, CreateUserRequest
from app import mongo

router = APIRouter()


@router.get("/users")
async def get_users() -> list[User]:
    return mongo.get_users()


@router.post("/users")
async def create_user(request: CreateUserRequest) -> User:
    return mongo.create_user(request.name, request.email)


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str) -> User:
    return mongo.get_user_by_id(user_id)


@router.put("/users/{user_id}")
async def update_user(user: User) -> User:
    return mongo.update_user(user)
