import hashlib
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class Author(BaseModel):
    id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: Optional[str]
    text: Optional[str]

    class Config:
        orm_mode = True


class PasswordPost(BaseModel):
    password: Optional[str]

    # validators
    _hash_password = validator("password", allow_reuse=True)(hash_password)


class CreatePost(PostBase, PasswordPost):
    author: Union[str, Author]

    @validator("author")
    def author_to_user_name_str(cls, v, values, **kwargs):
        return v.name if not isinstance(v, str) else v


class UpdatePost(PostBase, PasswordPost):
    pass


class DeletePost(PasswordPost):
    pass


class Post(PostBase):
    id: Optional[int]
    author: Optional[Author]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("author")
    def author_to_user_name_str(cls, author, values, **kwargs):
        return author.name if not isinstance(author, str) else author


class Comment(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    text: Optional[str]
    author: Union[str, Author]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

    @validator("author")
    def author_to_user_name_str(cls, v, values, **kwargs):
        return v.name if not isinstance(v, str) else v


class CreateComment(BaseModel):
    parent_id: Union[int, None] = None
    text: Optional[str]
    author: Union[str, Author]

    @validator("author")
    def author_to_user_name_str(cls, v, values, **kwargs):
        return v.name if not isinstance(v, str) else v


class ListComment(BaseModel):
    id: Optional[int]
    depth: Optional[int]
    text: Optional[str]
    author: Union[str, Author]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True

    @validator("author")
    def author_to_user_name_str(cls, v, values, **kwargs):
        return v.name if not isinstance(v, str) else v
