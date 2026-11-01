from pathlib import Path

from app.audio.transcription import transcriber


def main():

    audio_path = Path("tests/data/test.wav")

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Missing test audio: {audio_path}"
        )

    segments = transcriber.transcribe(
        audio_path,
        audio_offset=10.0,
        speaker="candidate",
    )

    print("\nTranscript segments:\n")

    for segment in segments:
        print(
            f"[{segment.start_time:.2f}s - "
            f"{segment.end_time:.2f}s] "
            f"{segment.speaker}: "
            f"{segment.text}"
        )


if __name__ == "__main__":
    main()