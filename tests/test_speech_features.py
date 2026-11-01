from app.domain.transcript_segment import TranscriptSegment
from app.speech.speech_feature_extractor import (
    speech_feature_extractor,
)


def main():

    segments = [
        TranscriptSegment(
            speaker="interviewer",
            start_time=0.0,
            end_time=4.0,
            text="Tell me about a difficult project.",
        ),
        TranscriptSegment(
            speaker="candidate",
            start_time=5.5,
            end_time=9.0,
            text="Um, I created the project plan.",
        ),
        TranscriptSegment(
            speaker="interviewer",
            start_time=9.5,
            end_time=11.0,
            text="What happened next?",
        ),
        TranscriptSegment(
            speaker="candidate",
            start_time=12.2,
            end_time=16.0,
            text="Uh, I coordinated with the team.",
        ),
    ]

    features = speech_feature_extractor.extract(
        segments,
        candidate_speaker="candidate",
    )

    print("\nSpeech features:\n")

    for name, value in features.items():
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()