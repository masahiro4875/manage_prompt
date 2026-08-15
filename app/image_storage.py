from pathlib import Path
from typing import Optional
from uuid import uuid4


UPLOAD_DIR = Path(__file__).resolve().parent / "uploads" / "images"


def save_image(
    contents: bytes,
    original_filename: Optional[str],
    upload_dir: Path = UPLOAD_DIR,
) -> str:
    """Save image bytes under a generated filename and return that filename."""
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(original_filename or "").name
    suffix = Path(suffix).suffix.lower()
    stored_filename = f"{uuid4()}{suffix}"

    destination = upload_dir / stored_filename
    destination.write_bytes(contents)

    return stored_filename
