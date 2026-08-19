from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    image_url: str
    is_thumbnail: Optional[bool] = False


class ImageCreate(ImageBase):
    prompt_id: UUID


class ImageOut(ImageBase):
    id: int
    prompt_id: UUID

    class Config:
        from_attributes = True

class ImageUploadOut(BaseModel):
    filename: str
    image_url: str

class ParameterBase(BaseModel):
    steps: Optional[int] = None
    sampler: Optional[str] = None
    cfg_scale: Optional[float] = None
    seed: Optional[int] = None


class ParameterCreate(ParameterBase):
    pass


class ParameterUpdate(ParameterBase):
    pass


class ParameterOut(ParameterBase):
    id: int
    prompt_id: UUID

    class Config:
        from_attributes = True


class PromptBase(BaseModel):
    title: Optional[str] = None
    prompt_text: str
    negative_prompt: Optional[str] = None
    memo: Optional[str] = None
    is_favorite: Optional[bool] = False


class PromptCreate(PromptBase):
    tag_names: List[str] = Field(default_factory=list)
    parameters: Optional[ParameterCreate] = None


class PromptUpdate(BaseModel):
    title: Optional[str] = None
    prompt_text: Optional[str] = None
    negative_prompt: Optional[str] = None
    memo: Optional[str] = None
    is_favorite: Optional[bool] = None
    tag_names: Optional[List[str]] = None
    parameters: Optional[ParameterUpdate] = None


class PromptOut(PromptBase):
    id: UUID
    tags: List[TagOut] = Field(default_factory=list)
    images: List[ImageOut] = Field(default_factory=list)
    parameters: Optional[ParameterOut] = None

    class Config:
        from_attributes = True  # SQLAlchemy対応
