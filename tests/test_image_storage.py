import tempfile
import unittest
from pathlib import Path
from uuid import UUID

from app.image_storage import save_image


class SaveImageTests(unittest.TestCase):
    def test_saves_contents_in_the_requested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory)

            stored_filename = save_image(b"image contents", "photo.png", upload_dir)

            self.assertEqual(
                (upload_dir / stored_filename).read_bytes(),
                b"image contents",
            )

    def test_generates_a_uuid_filename_and_preserves_the_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory)

            stored_filename = save_image(b"image contents", "photo.PNG", upload_dir)

            self.assertEqual(Path(stored_filename).suffix, ".png")
            UUID(Path(stored_filename).stem)

    def test_does_not_trust_a_path_in_the_original_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory) / "uploads"

            stored_filename = save_image(
                b"image contents",
                "../../outside.png",
                upload_dir,
            )

            self.assertEqual((upload_dir / stored_filename).parent, upload_dir)
            self.assertFalse((Path(temporary_directory) / "outside.png").exists())


if __name__ == "__main__":
    unittest.main()
