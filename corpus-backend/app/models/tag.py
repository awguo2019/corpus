from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.db import Base
from app.models.association import sticky_tag


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    parent_id = Column(Integer, ForeignKey("tags.id", ondelete="SET NULL"), nullable=True)

    parent = relationship("Tag", remote_side=[id], backref=backref("children"))
    stickies = relationship(
        "Sticky",
        secondary=sticky_tag,
        back_populates="tags",
        lazy="selectin",
        passive_deletes=True,
    )
