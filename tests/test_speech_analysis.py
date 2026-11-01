from datetime import datetime, timezone

from app.domain.response import Response
from app.domain.transcript_segment import TranscriptSegment
from app.services.speech_analysis_service import (
    speech_analysis_service,
)


def main():

    response = Response(
        question_id="Q1",
        transcript=(
            "Um, I created the project plan. "
            "Basically, I coordinated with the team."
        ),
        segments=[
            TranscriptSegment(
                speaker="candidate",
                start_time=0.0,
                end_time=4.0,
                text="Um, I created the project plan.",
            ),
            TranscriptSegment(
                speaker="candidate",
                start_time=5.5,
                end_time=9.0,
                text="Basically, I coordinated with the team.",
            ),
        ],
        started_at=datetime.now(timezone.utc),
        ended_at=datetime.now(timezone.utc),
        duration=9.0,
    )

    response = speech_analysis_service.analyze(
        response
    )

    print("\nSpeech features:")

    for name, value in response.speech_features.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()