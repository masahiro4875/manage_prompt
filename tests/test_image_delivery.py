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
                files={"file": ("photo.png", png_contents, "image/png")},
            )

            data = response.json()
            self.assertEqual(data["filename"], "generated.png")
            self.assertEqual(data["image_url"], "/uploads/images/generated.png")

    def test_uploaded_image_can_be_downloaded(self) -> None:
        pass

    def test_missing_uploaded_image_returns_404(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main()
