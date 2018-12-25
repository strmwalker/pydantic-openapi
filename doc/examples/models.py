from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

__all__ = ['User', 'Photo', 'Album', 'UserPhoto', 'UserArray']


class Photo(BaseModel):
    uid: UUID
    title: str


class User(BaseModel):
    username: str
    uid: UUID
    name: Optional[str]
    profile_photo: Optional[Photo]


class UserPhoto(BaseModel):
    uid: UUID
    user: User
    photo: Photo


class Album(BaseModel):
    uid: UUID
    user: User
    user_photos: List[UserPhoto]


class UserArray(BaseModel):
    user: User
    some_weird_list: List[int]
