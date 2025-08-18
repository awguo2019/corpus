from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
