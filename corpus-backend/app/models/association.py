from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db import Base

# Association table for many-to-many relationship between Stickies and Tags
sticky_tag = Table(
    "sticky_tag",
    Base.metadata,
    Column("sticky_id", ForeignKey("stickies.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
