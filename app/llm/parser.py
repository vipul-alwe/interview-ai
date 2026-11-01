import json


class LLMParser:

    @staticmethod
    def parse_json(text: str):

        start = text.find("{")

        if start == -1:
            raise ValueError("No JSON object found.")

        decoder = json.JSONDecoder()

        try:
            parsed, _ = decoder.raw_decode(
                text[start:]
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON returned by LLM: {exc}"
            ) from exc

        return parsed