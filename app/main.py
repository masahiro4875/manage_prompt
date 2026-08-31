from fastapi import FastAPI
from .routers import images, prompts, tags
from fastapi.staticfiles import StaticFiles
from .image_storage import UPLOAD_ROOT

UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

app = FastAPI()

app.include_router(images.router)
app.include_router(prompts.router)
app.include_router(tags.router)
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_ROOT),
    name="uploads"
)
