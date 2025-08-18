from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .tag import Tag


class StickyBase(BaseModel):
    title: str
    content: str
    url: Optional[str] = None


class StickyCreate(StickyBase):
    tag_ids: List[int] = Field(default_factory=list)


class StickyUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class Sticky(StickyBase):
    id: int
    like_count: int
    tags: List[Tag] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
