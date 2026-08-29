from pathlib import Path
from typing import Optional
from uuid import uuid4

UPLOAD_ROOT=Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR = UPLOAD_ROOT / "images"
ALLOWED_SUFFIXES = {".png"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_png(
    contents: bytes,
    original_filename: Optional[str],
) -> None:
    suffix = Path(original_filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise ValueError("Only PNG files are allowed")

    if not contents.startswith(PNG_SIGNATURE):
        raise ValueError("File content is not a valid PNG")


def save_image(
    contents: bytes,
    original_filename: Optional[str],
    upload_dir: Path = UPLOAD_DIR,
) -> str:
    """Save image bytes under a generated filename and return that filename."""
    validate_png(contents, original_filename)

    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(original_filename or "").name
    suffix = Path(suffix).suffix.lower()
    stored_filename = f"{uuid4()}{suffix}"

    destination = upload_dir / stored_filename
    destination.write_bytes(contents)

    return stored_filename
