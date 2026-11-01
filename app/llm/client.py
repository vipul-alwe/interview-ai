import time
from typing import Any

from llama_cpp import Llama

from app.config.settings import (
    LLM_CONTEXT,
    LLM_GPU_LAYERS,
    LLM_MAX_TOKENS,
    LLM_MODEL,
    LLM_TEMPERATURE,
)


class LLMClient:

    def __init__(self):
        self._llm = None

    def _load(self):

        if self._llm is not None:
            return

        print(
            f"[LLM] Loading model: "
            f"{LLM_MODEL}"
        )

        start = time.monotonic()

        self._llm = Llama(
            model_path=str(LLM_MODEL),
            n_ctx=LLM_CONTEXT,
            n_gpu_layers=LLM_GPU_LAYERS,
            verbose=False,
        )

        elapsed = (
            time.monotonic()
            - start
        )

        print(
            "[LLM] Model loaded "
            f"({elapsed:.1f}s)."
        )

    def _prompt_tokens(
        self,
        prompt: str,
    ) -> int:

        try:

            return len(
                self._llm.tokenize(
                    prompt.encode(
                        "utf-8"
                    ),
                    add_bos=True,
                    special=False,
                )
            )

        except Exception:

            return 0

    def generate(
        self,
        prompt: str,
    ) -> str:

        self._load()

        prompt_tokens = (
            self._prompt_tokens(
                prompt
            )
        )

        print(
            "[LLM] Generation started "
            f"| prompt: "
            f"{prompt_tokens} tokens"
        )

        start = time.monotonic()

        output = self._llm.create_completion(
            prompt=prompt,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
        )

        elapsed = (
            time.monotonic()
            - start
        )

        text = (
            output["choices"][0]["text"]
            .strip()
        )

        generated_tokens = 0

        try:

            generated_tokens = (
                output["usage"]
                .get(
                    "completion_tokens",
                    0,
                )
            )

        except Exception:
            pass

        print(
            "[LLM] Generation complete "
            f"| {elapsed:.1f}s "
            f"| output: "
            f"{generated_tokens} tokens"
        )

        return text

    def generate_json(
        self,
        prompt: str,
        schema: dict[str, Any],
    ) -> str:

        self._load()

        prompt_tokens = (
            self._prompt_tokens(
                prompt
            )
        )

        print(
            "[LLM] JSON generation started "
            f"| prompt: "
            f"{prompt_tokens} tokens"
        )

        start = time.monotonic()

        output = (
            self._llm.create_chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                response_format={
                    "type": "json_object",
                    "schema": schema,
                },
                max_tokens=LLM_MAX_TOKENS,
                temperature=LLM_TEMPERATURE,
            )
        )

        elapsed = (
            time.monotonic()
            - start
        )

        text = (
            output["choices"][0]["message"][
                "content"
            ]
            .strip()
        )

        generated_tokens = 0

        try:

            generated_tokens = (
                output["usage"]
                .get(
                    "completion_tokens",
                    0,
                )
            )

        except Exception:
            pass

        print(
            "[LLM] JSON generation complete "
            f"| {elapsed:.1f}s "
            f"| output: "
            f"{generated_tokens} tokens"
        )

        return text


llm_client = LLMClient()