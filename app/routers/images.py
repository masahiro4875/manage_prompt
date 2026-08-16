from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..db import get_db
from ..image_storage import save_image

router = APIRouter(prefix="/images", tags=["images"])

MAX_FILESIZE = 20 * 1024 * 1024


@router.get("/", response_model=List[schemas.ImageOut])
def get_images(q: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Image).join(models.Prompt)

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            or_(
                models.Prompt.title.ilike(pattern),
                models.Prompt.prompt_text.ilike(pattern),
                models.Prompt.negative_prompt.ilike(pattern),
                models.Prompt.memo.ilike(pattern),
                models.Prompt.tags.any(models.Tag.name.ilike(pattern)),
            )
        )

    return query.order_by(models.Image.created_at.desc()).all()


@router.post("/", response_model=schemas.ImageOut)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    prompt = db.query(models.Prompt).filter(models.Prompt.id == image.prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    db_image = models.Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> dict[str, str]:
    contents = await file.read(MAX_FILESIZE + 1)

    if len(contents) > MAX_FILESIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must be 20 MB or smaller",
        )

    try:
        stored_filename = save_image(contents, file.filename)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"filename": stored_filename}


@router.get("/{image_id}", response_model=schemas.ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(models.Image).filter(models.Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    db.delete(image)
    db.commit()
    return {"message": "deleted"}
