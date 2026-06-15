from fastapi import FastAPI
from .routers import images, prompts, tags

app = FastAPI()

app.include_router(images.router)
app.include_router(prompts.router)
app.include_router(tags.router)
