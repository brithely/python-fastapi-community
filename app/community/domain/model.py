import hashlib
from datetime import datetime
from typing import Optional

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
    _hash_password = validator('password', allow_reuse=True)(hash_password)


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
