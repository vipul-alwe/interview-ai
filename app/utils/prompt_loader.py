from pathlib import Path

from app.config.settings import PROMPTS_DIR


class PromptLoader:

    _cache = {}

    @classmethod
    def load(cls, filename: str) -> str:

        if filename in cls._cache:
            return cls._cache[filename]

        path = PROMPTS_DIR / filename

        prompt = path.read_text(encoding="utf-8")

        cls._cache[filename] = prompt

        return prompt