import tempfile
import unittest
from pathlib import Path
from uuid import UUID

from app.image_storage import PNG_SIGNATURE, save_image, validate_png


VALID_PNG_CONTENTS = PNG_SIGNATURE + b"image contents"


class ValidatePngTests(unittest.TestCase):
    def test_accepts_a_png_with_an_uppercase_suffix(self) -> None:
        result = validate_png(VALID_PNG_CONTENTS, "photo.PNG")

        self.assertIsNone(result)

    def test_rejects_a_non_png_suffix(self) -> None:
        with self.assertRaisesRegex(ValueError, "Only PNG files are allowed"):
            validate_png(VALID_PNG_CONTENTS, "photo.jpg")

    def test_rejects_contents_without_the_png_signature(self) -> None:
        with self.assertRaisesRegex(ValueError, "not a valid PNG"):
            validate_png(b"not a PNG", "photo.png")

    def test_rejects_a_missing_filename(self) -> None:
        with self.assertRaisesRegex(ValueError, "Only PNG files are allowed"):
            validate_png(VALID_PNG_CONTENTS, None)


class SaveImageTests(unittest.TestCase):
    def test_saves_contents_in_the_requested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory)

            stored_filename = save_image(
                VALID_PNG_CONTENTS,
                "photo.png",
                upload_dir,
            )

            self.assertEqual(
                (upload_dir / stored_filename).read_bytes(),
                VALID_PNG_CONTENTS,
            )

    def test_generates_a_uuid_filename_and_preserves_the_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory)

            stored_filename = save_image(
                VALID_PNG_CONTENTS,
                "photo.PNG",
                upload_dir,
            )

            self.assertEqual(Path(stored_filename).suffix, ".png")
            UUID(Path(stored_filename).stem)

    def test_does_not_trust_a_path_in_the_original_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory) / "uploads"

            stored_filename = save_image(
                VALID_PNG_CONTENTS,
                "../../outside.png",
                upload_dir,
            )

            self.assertEqual((upload_dir / stored_filename).parent, upload_dir)
            self.assertFalse((Path(temporary_directory) / "outside.png").exists())

    def test_does_not_create_a_file_when_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            upload_dir = Path(temporary_directory) / "uploads"

            with self.assertRaises(ValueError):
                save_image(b"not a PNG", "photo.png", upload_dir)

            self.assertFalse(upload_dir.exists())


if __name__ == "__main__":
    unittest.main()
