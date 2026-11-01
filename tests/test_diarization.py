from pathlib import Path

from app.audio.diarization import diarizer


AUDIO_PATH = Path(
    "temp_audio/interview.wav"
)


def main():

    if not AUDIO_PATH.exists():
        raise FileNotFoundError(
            AUDIO_PATH
        )

    print(
        "Running speaker diarization..."
    )

    segments = diarizer.diarize(
        AUDIO_PATH,
        min_speakers=2,
        max_speakers=5,
    )

    print(
        "\n" + "=" * 80
    )

    print(
        "DIARIZATION RESULTS"
    )

    print(
        "=" * 80
    )

    for segment in segments:

        print(
            f"{segment['start_time']:8.2f} - "
            f"{segment['end_time']:8.2f} | "
            f"{segment['speaker']}"
        )

    speakers = sorted(
        {
            segment["speaker"]
            for segment in segments
        }
    )

    print(
        "\nSpeakers detected:"
    )

    for speaker in speakers:
        print(
            f"  {speaker}"
        )

    print(
        f"\nTotal speakers: "
        f"{len(speakers)}"
    )


if __name__ == "__main__":
    main()