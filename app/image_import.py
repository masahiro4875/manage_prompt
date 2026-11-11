from sqlalchemy.orm import Session
from . import models
from .image_metadata import extract_prompts_from_bytes


def create_prompt_from_image(
    contents: bytes,
    db: Session,
) -> models.Prompt:
    # ① 画像からプロンプトを抽出する
    prompt_data = extract_prompts_from_bytes(contents)

    # ② 抽出結果から models.Prompt を作る
    prompt = models.Prompt(**prompt_data)

    # ③ db.add() で登録対象にする
    db.add(prompt)

    # ④ db.flush() でDBに反映し、IDを取得できるようにする
    db.flush()
    # ⑤ 作ったPromptをreturnする
    return prompt
