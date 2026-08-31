import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.image_storage import PNG_SIGNATURE

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
                file={"files": ("photo.png", png_contents, "image/png")},
            )
            self.assertEqual(response.status_code, 200, response.text)
            self.assertIn("filename", response.json())
            self.assertIn("image_url", response.json())

    def test_uploaded_image_can_be_downloaded(self) -> None:
        pass

    def test_missing_uploaded_image_returns_404(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
