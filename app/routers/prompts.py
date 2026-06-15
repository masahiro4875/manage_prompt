from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from .. import models, schemas
from ..db import get_db

router = APIRouter(prefix="/prompts", tags=["prompts"])


def get_prompt_or_404(prompt_id: UUID, db: Session):
    prompt = db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def get_or_create_tags(tag_names: List[str], db: Session):
    tags = []
    for name in tag_names:
        clean_name = name.strip()
        if not clean_name:
            continue

        tag = db.query(models.Tag).filter(models.Tag.name == clean_name).first()
        if not tag:
            tag = models.Tag(name=clean_name)
            db.add(tag)
        tags.append(tag)
    return tags


# CREATE
@router.post("/", response_model=schemas.PromptOut)
def create_prompt(prompt: schemas.PromptCreate, db: Session = Depends(get_db)):
    data = prompt.model_dump(exclude={"tag_names", "parameters"})
    db_prompt = models.Prompt(**data)
    db_prompt.tags = get_or_create_tags(prompt.tag_names, db)

    if prompt.parameters:
        db_prompt.parameters = models.Parameter(**prompt.parameters.model_dump())

    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


# READ ALL（検索付き）
@router.get("/", response_model=List[schemas.PromptOut])
def get_prompts(q: str = "", db: Session = Depends(get_db)):
    query = db.query(models.Prompt)

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

    return query.order_by(models.Prompt.created_at.desc()).all()


# READ ONE
@router.get("/{prompt_id}", response_model=schemas.PromptOut)
def get_prompt(prompt_id: UUID, db: Session = Depends(get_db)):
    return get_prompt_or_404(prompt_id, db)


# UPDATE
@router.put("/{prompt_id}", response_model=schemas.PromptOut)
def update_prompt(prompt_id: UUID, update: schemas.PromptUpdate, db: Session = Depends(get_db)):
    prompt = get_prompt_or_404(prompt_id, db)

    update_data = update.model_dump(exclude_unset=True)
    tag_names = update_data.pop("tag_names", None)
    parameter_data = update_data.pop("parameters", None)

    for key, value in update_data.items():
        setattr(prompt, key, value)

    if tag_names is not None:
        prompt.tags = get_or_create_tags(tag_names, db)

    if parameter_data is not None:
        if prompt.parameters:
            for key, value in parameter_data.items():
                setattr(prompt.parameters, key, value)
        else:
            prompt.parameters = models.Parameter(**parameter_data)

    db.commit()
    db.refresh(prompt)
    return prompt


# DELETE
@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: UUID, db: Session = Depends(get_db)):
    prompt = get_prompt_or_404(prompt_id, db)

    db.delete(prompt)
    db.commit()
    return {"message": "deleted"}
