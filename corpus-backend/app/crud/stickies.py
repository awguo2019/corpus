from typing import List, Sequence, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.models import Sticky as StickyModel, Tag as TagModel


def create_sticky(session: Session, *, title: str, content: str, url: Optional[str], tag_ids: Optional[List[int]]) -> StickyModel:
    sticky = StickyModel(title=title, content=content, url=url)
    if tag_ids:
        ids = list(set(tag_ids))
        tags: Sequence[TagModel] = session.query(TagModel).filter(TagModel.id.in_(ids)).all()
        if len(tags) != len(ids):
            found_ids = {t.id for t in tags}
            missing = [i for i in ids if i not in found_ids]
            raise HTTPException(status_code=422, detail={"missing_tag_ids": missing})
        sticky.tags = list(tags)
    session.add(sticky)
    session.commit()
    session.refresh(sticky)
    return sticky


def list_stickies(session: Session, *, limit: int = 100, offset: int = 0) -> List[StickyModel]:
    return (
        session.query(StickyModel)
        .options(selectinload(StickyModel.tags))
        .offset(offset)
        .limit(limit)
        .all()
    )


def like_sticky(session: Session, sticky_id: int) -> StickyModel:
    sticky = session.get(StickyModel, sticky_id)
    if not sticky:
        raise HTTPException(status_code=404, detail="Sticky not found")
    sticky.like_count += 1
    session.commit()
    session.refresh(sticky)
    return sticky


def get_sticky(session: Session, sticky_id: int) -> StickyModel:
    sticky = session.get(
        StickyModel,
        sticky_id,
        options=(selectinload(StickyModel.tags),),
    )
    if not sticky:
        raise HTTPException(status_code=404, detail="Sticky not found")
    return sticky


def update_sticky(
    session: Session,
    sticky_id: int,
    *,
    title: Optional[str] = None,
    content: Optional[str] = None,
    url: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
) -> StickyModel:
    sticky = session.get(StickyModel, sticky_id)
    if not sticky:
        raise HTTPException(status_code=404, detail="Sticky not found")
    if title is not None:
        sticky.title = title
    if content is not None:
        sticky.content = content
    if url is not None:
        sticky.url = url
    if tag_ids is not None:
        ids = list(set(tag_ids))
        if ids:
            tags: Sequence[TagModel] = session.query(TagModel).filter(TagModel.id.in_(ids)).all()
            if len(tags) != len(ids):
                found_ids = {t.id for t in tags}
                missing = [i for i in ids if i not in found_ids]
                raise HTTPException(status_code=422, detail={"missing_tag_ids": missing})
            sticky.tags = list(tags)
        else:
            sticky.tags = []
    session.commit()
    session.refresh(sticky)
    return sticky


def delete_sticky(session: Session, sticky_id: int) -> None:
    sticky = session.get(StickyModel, sticky_id)
    if not sticky:
        raise HTTPException(status_code=404, detail="Sticky not found")
    session.delete(sticky)
    session.commit()
