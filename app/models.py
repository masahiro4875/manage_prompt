from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    Table,
    Text,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .db import Base

prompt_tags = Table(
    "prompt_tags",
    Base.metadata,
    Column(
        "prompt_id",
        UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    prompt_text = Column(Text, nullable=False)
    negative_prompt = Column(Text)
    memo = Column(Text)
    is_favorite = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    tags = relationship("Tag", secondary=prompt_tags, back_populates="prompts")
    images = relationship(
        "Image", back_populates="prompt", cascade="all, delete-orphan"
    )
    parameters = relationship(
        "Parameter",
        back_populates="prompt",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    prompts = relationship("Prompt", secondary=prompt_tags, back_populates="tags")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    prompt_id = Column(
        UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False
    )
    image_url = Column(Text, nullable=False)
    is_thumbnail = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    prompt = relationship("Prompt", back_populates="images")


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(Integer, primary_key=True)
    prompt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    steps = Column(Integer)
    sampler = Column(Text)
    cfg_scale = Column(Float)
    seed = Column(BigInteger)

    prompt = relationship("Prompt", back_populates="parameters")

