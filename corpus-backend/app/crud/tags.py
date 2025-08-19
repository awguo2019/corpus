from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Tag as TagModel


def create_tag(session: Session, *, name: str, parent_id: Optional[int] = None) -> TagModel:
    # Ensure name is unique
    if session.query(TagModel).filter_by(name=name).first():
        raise HTTPException(status_code=400, detail="Tag with this name already exists")

    tag = TagModel(name=name, parent_id=parent_id)
    session.add(tag)
    try:
        session.commit()
        session.refresh(tag)
        return tag
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invalid parent_id or constraint violation")


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
        # Check for unique name conflict
        existing = session.query(TagModel).filter(TagModel.name == name, TagModel.id != tag_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Another tag with this name already exists")
        tag.name = name

    if parent_id is not None:
        # Optional: validate parent exists
        if parent_id == tag_id:
            raise HTTPException(status_code=400, detail="Tag cannot be its own parent")
        if not session.get(TagModel, parent_id):
            raise HTTPException(status_code=400, detail="Parent tag not found")
        tag.parent_id = parent_id

    try:
        session.commit()
        session.refresh(tag)
        return tag
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Invalid update (constraint violation)")


def delete_tag(session: Session, tag_id: int) -> None:
    tag = session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Set children to null parent first
    session.query(TagModel).filter(TagModel.parent_id == tag_id).update(
        {TagModel.parent_id: None}, synchronize_session=False
    )

    session.delete(tag)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Could not delete tag due to constraints")
