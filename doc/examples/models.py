from typing import Optional
from uuid import UUID

from pydantic import BaseModel

__all__ = ['User', 'Photo']


class Photo(BaseModel):
    uid: UUID
    title: str


class User(BaseModel):
    username: str
    uid: UUID
    name: Optional[str]
    photo: Optional[Photo]
