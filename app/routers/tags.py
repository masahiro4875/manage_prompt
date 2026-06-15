from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[schemas.TagOut])
def get_tags(db: Session = Depends(get_db)):
    return db.query(models.Tag).order_by(models.Tag.name.asc()).all()


@router.post("/", response_model=schemas.TagOut)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    clean_name = tag.name.strip()
    if not clean_name:
        raise HTTPException(status_code=400, detail="Tag name is required")

    existing = db.query(models.Tag).filter(models.Tag.name == clean_name).first()
    if existing:
        return existing

    db_tag = models.Tag(name=clean_name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"message": "deleted"}
