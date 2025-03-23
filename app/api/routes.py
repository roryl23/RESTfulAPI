from fastapi import APIRouter, status, Response
from opentelemetry import trace

from app.models import User, UserRequest, PostRequest, Post
from app import mongo

router = APIRouter()


@router.get("/users")
async def get_users() -> list[User]:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    return mongo.get_users()


@router.post("/users")
async def create_user(request: UserRequest) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.create_record(
        'users',
        {
            'name': request.name,
            'email': request.email,
        }
    )
    if result:
        user = mongo.get_user_by_id(str(result.inserted_id))
        if user:
            return Response(
                content=user.model_dump_json(),
                status_code=status.HTTP_201_CREATED,
                media_type="application/json",
            )
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.get_user_by_id(user_id)
    if result:
        return Response(
            content=result.model_dump_json(),
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/users/{user_id}")
async def update_user(user_id: str, request: UserRequest) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.update_record(
        'users',
        {
            '_id': user_id,
            'name': request.name,
            'email': request.email,
        },
    )
    if result:
        user = mongo.get_user_by_id(user_id)
        if user:
            return Response(
                content=user.model_dump_json(),
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif result is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/users/{user_id}")
async def delete_user(user_id: str) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.delete_record('users', user_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/posts")
async def get_posts() -> list[Post]:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    return mongo.get_posts()


@router.post("/posts")
async def create_post(request: PostRequest) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    user = mongo.get_user_by_id(request.user_id)
    if user:
        result = mongo.create_record(
            'posts',
            {
                'title': request.title,
                'content': request.content,
                'user_id': request.user_id,
            }
        )
        post = mongo.get_post_by_id(str(result.inserted_id))
        if post:
            return Response(
                content=post.model_dump_json(),
                status_code=status.HTTP_201_CREATED,
                media_type="application/json",
            )
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/posts/{post_id}")
async def get_post_by_id(post_id: str) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.get_post_by_id(post_id)
    if result:
        return Response(
            content=result.model_dump_json(),
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/posts/{post_id}")
async def update_post(post_id: str, request: PostRequest) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.update_record(
        'posts',
        {
            '_id': post_id,
            'title': request.title,
            'content': request.content,
            'user_id': request.user_id,
        },
    )
    if result:
        post = mongo.get_post_by_id(post_id)
        if post:
            return Response(
                content=post.model_dump_json(),
                status_code=status.HTTP_200_OK,
                media_type="application/json",
            )
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: str) -> Response:
    span = trace.get_current_span()
    span.set_attribute("resource", "mongo")
    result = mongo.delete_record('posts', post_id)
    if result:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)