import unittest
from io import BytesIO
from unittest.mock import patch

from fastapi import HTTPException, UploadFile

from app.image_storage import PNG_SIGNATURE
from app.routers.images import upload_image


class UploadImageRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_400_for_an_invalid_png(self) -> None:
        upload = UploadFile(
            file=BytesIO(b"not a PNG"),
            filename="photo.png",
        )

        with self.assertRaises(HTTPException) as raised:
            await upload_image(upload)

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.detail, "File content is not a valid PNG")

    async def test_returns_413_when_file_exceeds_the_size_limit(self) -> None:
        with patch("app.routers.images.MAX_FILESIZE", 8):
            upload = UploadFile(
                file=BytesIO(PNG_SIGNATURE + b"x"),
                filename="photo.png",
            )

            with self.assertRaises(HTTPException) as raised:
                await upload_image(upload)

        self.assertEqual(raised.exception.status_code, 413)
        self.assertEqual(
            raised.exception.detail,
            "File size must be 20 MB or smaller",
        )


if __name__ == "__main__":
    unittest.main()
