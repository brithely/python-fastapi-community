import hashlib
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class Author(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    author: Union[str, Author]

    @validator("author")
    def author_to_name_str(cls, v, values, **kwargs):
        return v.name if not isinstance(v, str) else v


class Post(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True


class PasswordPost(BaseModel):
    password: str

    # validators
    _hash_password = validator("password", allow_reuse=True)(hash_password)


class CreatePost(
    PasswordPost,
    AuthorBase,
    Post,
):
    pass


class UpdatePost(PasswordPost, Post):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "title": "title",
                "text": "Very Nice",
                "password": "password",
            }
        }


class DeletePost(PasswordPost):
    pass


class ListPost(AuthorBase, Post):
    id: int
    created_at: datetime
    updated_at: datetime


class Comment(AuthorBase, BaseModel):
    id: int
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateComment(AuthorBase, BaseModel):
    parent_id: Optional[int]
    text: str

    class Config:
        schema_extra = {
            "example": {
                "author": "author",
                "text": "Very Nice",
            }
        }


class ListComment(Comment):
    depth: int
