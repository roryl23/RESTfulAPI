from fastapi import APIRouter, status, Response

from app.models import User, CreateUserRequest
from app import mongo

router = APIRouter()


@router.get("/users")
async def get_users() -> list[User]:
    return mongo.get_users()


@router.post("/users")
async def create_user(request: CreateUserRequest) -> User:
    result = mongo.create_record(
        'users',
        {
            'name': request.name,
            'email': request.email,
        }
    )
    return mongo.get_user_by_id(str(result.inserted_id))


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str) -> User:
    return mongo.get_user_by_id(user_id)


@router.put("/users/{user_id}")
async def update_user(user: User) -> User:
    return mongo.update_user(user)


@router.delete("/users/{user_id}")
async def delete_user(user_id: str) -> Response:
    result = mongo.delete_record('users', user_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/posts")
async def get_posts() -> list[User]:
    return mongo.get_posts()


@router.post("/posts")
async def create_post(request: CreateUserRequest) -> User:
    return mongo.create_post(request.name, request.email)


@router.get("/posts/{post_id}")
async def get_post_by_id(post_id: str) -> User:
    return mongo.get_doc_by_id(post_id)


@router.put("/posts/{post_id}")
async def update_post(post: User) -> User:
    return mongo.update_post(post)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: str) -> Response:
    result = mongo.delete_record('posts', post_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)