import json

from pathlib import Path
from io import BytesIO

from PIL import Image
from PIL.PngImagePlugin import PngInfo


def inspect_metadata(input_path: Path) -> None:
    with Image.open(input_path) as image:
        metadata = PngInfo()

        for key, value in image.info.items():
            if key == "Comment":
                data = json.loads(value)
                caption = data["v4_prompt"]["caption"]

                base_prompt = caption["base_caption"]
                negative_caption = data["v4_negative_prompt"]["caption"]["base_caption"]

                print("Base prompt:", base_prompt)
                print("Negative prompt:", negative_caption)

                for index, character in enumerate(caption["char_captions"], start=1):
                    character_prompt = character["char_caption"]
                    print(f"Character {index}:", character_prompt)


def extract_base_prompt(input_path: Path) -> str:
    with Image.open(input_path) as image:
        comment = image.info["Comment"]
        data = json.loads(comment)

        return data["v4_prompt"]["caption"]["base_caption"]


def extract_negative_prompt(input_path: Path) -> str:

    with Image.open(input_path) as image:
        comment = image.info["Comment"]
        data = json.loads(comment)

        return data["v4_negative_prompt"]["caption"]["base_caption"]


def extract_character_prompt(input_path: Path) -> list[str]:

    with Image.open(input_path) as image:
        comment = image.info["Comment"]
        data = json.loads(comment)
        characters = data["v4_prompt"]["caption"]["char_captions"]

        prompts: list[str] = []

        for character in characters:
            prompts.append(character["char_caption"])

        return prompts



def extract_prompts_from_bytes(contents: bytes) -> dict[str, object]:
    with Image.open(BytesIO(contents)) as image:
        comment = image.info["Comment"]
        data = json.loads(comment)
        characters = data["v4_prompt"]["caption"]["char_captions"]

        base_prompt = data["v4_prompt"]["caption"]["base_caption"]
        negative_prompt = data["v4_negative_prompt"]["caption"]["base_caption"]

        character_prompts: list[str] = []

        for character in characters:
            character_prompts.append(character["char_caption"])

        return {
            "base_prompt": base_prompt,
            "base_negative_prompt": negative_prompt,
            "character_prompts": character_prompts,
        }

def extract_prompts(input_path: Path) -> dict[str, object]:
    return extract_prompts_from_bytes(input_path.read_bytes())


if __name__ == "__main__":
    input_path = Path("uploads/images/test.png")
    contents = input_path.read_bytes()

    expected = extract_prompts(input_path)
    actual = extract_prompts_from_bytes(contents)

    assert expected == actual
