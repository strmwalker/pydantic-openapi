from pydantic import BaseModel

__all__ = ['Photo']


class Photo(BaseModel):
    id: int
