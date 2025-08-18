from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    Sticky as StickySchema,
    StickyCreate as StickyCreateSchema,
    StickyUpdate as StickyUpdateSchema,
)
from app.crud.stickies import (
    create_sticky as create_sticky_crud,
    list_stickies as list_stickies_crud,
    like_sticky as like_sticky_crud,
    get_sticky as get_sticky_crud,
    update_sticky as update_sticky_crud,
    delete_sticky as delete_sticky_crud,
)

router = APIRouter(prefix="/stickies", tags=["stickies"])

@router.post("/", response_model=StickySchema)
def create_sticky(sticky: StickyCreateSchema, db: Session = Depends(get_db)):
    return create_sticky_crud(
        db,
        title=sticky.title,
        content=sticky.content,
        url=sticky.url,
        tag_ids=sticky.tag_ids,
    )

@router.get("/", response_model=List[StickySchema])
def list_stickies(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return list_stickies_crud(db, limit=limit, offset=offset)

@router.post("/{sticky_id}/like")
def like_sticky(sticky_id: int, db: Session = Depends(get_db)):
    sticky = like_sticky_crud(db, sticky_id)
    return {"id": sticky.id, "like_count": sticky.like_count}


@router.get("/{sticky_id}", response_model=StickySchema)
def get_sticky(sticky_id: int, db: Session = Depends(get_db)):
    return get_sticky_crud(db, sticky_id)


@router.patch("/{sticky_id}", response_model=StickySchema)
def update_sticky(sticky_id: int, patch: StickyUpdateSchema, db: Session = Depends(get_db)):
    return update_sticky_crud(
        db,
        sticky_id,
        title=patch.title,
        content=patch.content,
        url=patch.url,
        tag_ids=patch.tag_ids,
    )


@router.delete("/{sticky_id}", status_code=204)
def delete_sticky(sticky_id: int, db: Session = Depends(get_db)):
    delete_sticky_crud(db, sticky_id)
    return None
