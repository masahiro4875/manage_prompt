import json
from io import BytesIO

import unittest

from PIL import Image
from PIL.PngImagePlugin import PngInfo

from app.image_metadata import extract_prompts_from_bytes


class ImageMetadataExtract(unittest.TestCase):
    def test_metadata_extract(self) -> None:
        data = {
            "v4_prompt": {
                "caption": {
                    "base_caption": "base prompt",
                    "char_captions": [
                        {"char_caption": "character one"},
                        {"char_caption": "character two"},
                    ],
                }
            },
            "v4_negative_prompt": {
                "caption": {
                    "base_caption": "",
                }
            },
        }

        metadata = PngInfo()
        metadata.add_text("Comment", json.dumps(data))

        buffer = BytesIO()
        Image.new("RGB", (1, 1)).save(
            buffer,
            format="PNG",
            pnginfo=metadata,
        )

        result = extract_prompts_from_bytes(buffer.getvalue())

        self.assertEqual(
            result["character_prompts"],
            ["character one", "character two"],
        )
        self.assertEqual(result["base_prompt"], "base prompt")

        self.assertEqual(result["base_negative_prompt"], "")
