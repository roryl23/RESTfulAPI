from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    name: str
    email: str


class CreateUserRequest(BaseModel):
    name: str
    email: str


class Post(BaseModel):
    post_id: str
    title: str
    content: str
    user_id: str


class CreatePostRequest(BaseModel):
    title: str
    content: str
    user_id: str
