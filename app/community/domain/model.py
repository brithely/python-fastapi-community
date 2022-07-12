import hashlib
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


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
    user_name: Optional[str]


class UpdatePost(PostBase, PasswordPost):
    pass


class DeletePost(PasswordPost):
    pass


class Post(PostBase):
    id: Optional[int]
    user_name: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Comment(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    text: Optional[str]
    user_name: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class CreateComment(BaseModel):
    parent_id: Union[int, None] = None
    text: Optional[str]
    user_name: Optional[str]


class ListComment(BaseModel):
    id: Optional[int]
    depth: Optional[int]
    text: Optional[str]
    user_name: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
