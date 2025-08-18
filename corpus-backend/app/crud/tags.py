from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Tag as TagModel


def create_tag(session: Session, *, name: str, parent_id: Optional[int]) -> TagModel:
    tag = TagModel(name=name, parent_id=parent_id)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


def list_tags(session: Session, *, limit: int = 100, offset: int = 0) -> List[TagModel]:
    return (
        session.query(TagModel)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_tag(session: Session, tag_id: int) -> TagModel:
    tag = session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


def update_tag(
    session: Session,
    tag_id: int,
    *,
    name: Optional[str] = None,
    parent_id: Optional[int] = None,
) -> TagModel:
    tag = session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if name is not None:
        tag.name = name
    if parent_id is not None:
        tag.parent_id = parent_id
    session.commit()
    session.refresh(tag)
    return tag


def delete_tag(session: Session, tag_id: int) -> None:
    tag = session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
