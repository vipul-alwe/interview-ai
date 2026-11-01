from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    speaker: str

    start_time: float

    end_time: float

    text: str