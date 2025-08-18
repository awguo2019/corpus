from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import Tag as TagSchema, TagCreate as TagCreateSchema, TagUpdate as TagUpdateSchema
from app.crud.tags import (
    create_tag as create_tag_crud,
    list_tags as list_tags_crud,
    get_tag as get_tag_crud,
    update_tag as update_tag_crud,
    delete_tag as delete_tag_crud,
)

router = APIRouter(prefix="/tags", tags=["tags"])

@router.post("/", response_model=TagSchema)
def create_tag(tag: TagCreateSchema, session: Session = Depends(get_db)):
    return create_tag_crud(session, name=tag.name, parent_id=tag.parent_id)

@router.get("/", response_model=List[TagSchema])
def list_tags(limit: int = 100, offset: int = 0, session: Session = Depends(get_db)):
    return list_tags_crud(session, limit=limit, offset=offset)

@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, session: Session = Depends(get_db)):
    return get_tag_crud(session, tag_id)


@router.patch("/{tag_id}", response_model=TagSchema)
def update_tag(tag_id: int, patch: TagUpdateSchema, session: Session = Depends(get_db)):
    return update_tag_crud(session, tag_id, name=patch.name, parent_id=patch.parent_id)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, session: Session = Depends(get_db)):
    delete_tag_crud(session, tag_id)
    return None
