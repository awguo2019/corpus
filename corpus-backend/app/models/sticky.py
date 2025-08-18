from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base
from app.models.association import sticky_tag


class Sticky(Base):
    __tablename__ = "stickies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(1000))
    url = Column(String, nullable=True)
    like_count = Column(Integer, default=0)

    tags = relationship(
        "Tag",
        secondary=sticky_tag,
        back_populates="stickies",
        lazy="selectin",
        passive_deletes=True,
    )
