import unittest
from unittest.mock import patch
from uuid import uuid4
from fastapi.testclient import TestClient

from app.main import app
from app.image_storage import PNG_SIGNATURE, UPLOAD_ROOT


png_contents = PNG_SIGNATURE + b"image contents"


class ImageDeliveryTests(unittest.TestCase):
    def test_upload_response_contains_image_url(self) -> None:
        client = TestClient(app)

        with patch(
            "app.routers.images.save_image",
            return_value="generated.png",
        ):
            response = client.post(
                "/images/upload",
                files={"file": ("photo.png", png_contents, "image/png")},
            )

            data = response.json()
            self.assertEqual(data["filename"], "generated.png")
            self.assertEqual(data["image_url"], "/uploads/images/generated.png")

    def test_uploaded_image_can_be_downloaded(self) -> None:
        client = TestClient(app)

        # preparing file for testing
        file_name = f"test-{uuid4()}.png"
        destination = UPLOAD_ROOT / "images" / file_name

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.addCleanup(
            destination.unlink,
            missing_ok=True,
        )

        destination.write_bytes(png_contents)

        response = client.get(f"/uploads/images/{file_name}")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.content, png_contents, response.text)

    def test_missing_uploaded_image_returns_404(self) -> None:
        client = TestClient(app)

        response = client.get("/uploads/images/missing.png")

        self.assertEqual(response.status_code, 404, response.text)


if __name__ == "__main__":
    unittest.main()
