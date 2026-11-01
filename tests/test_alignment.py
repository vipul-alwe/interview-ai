from pathlib import Path

from app.audio.transcription import (
    transcriber,
)

from app.audio.diarization import (
    diarizer,
)

from app.audio.transcript_aligner import (
    transcript_aligner,
)


AUDIO_PATH = Path(
    "temp_audio/interview.wav"
)


def main():

    print(
        "Transcribing interview..."
    )

    transcript_segments = (
        transcriber.transcribe_file(
            AUDIO_PATH
        )
    )

    print(
        f"Whisper segments: "
        f"{len(transcript_segments)}"
    )

    print(
        "\nRunning diarization..."
    )

    diarization_segments = (
        diarizer.diarize(
            AUDIO_PATH,
            min_speakers=2,
            max_speakers=5,
        )
    )

    print(
        f"Diarization segments: "
        f"{len(diarization_segments)}"
    )

    print(
        "\nAligning Whisper + diarization..."
    )

    aligned = (
        transcript_aligner.align(
            transcript_segments,
            diarization_segments,
        )
    )

    print(
        "\n" + "=" * 90
    )

    print(
        "ALIGNED TRANSCRIPT"
    )

    print(
        "=" * 90
    )

    for segment in aligned:

        print(
            f"{segment.start_time:8.2f} - "
            f"{segment.end_time:8.2f} | "
            f"{segment.speaker:12} | "
            f"{segment.text}"
        )

    print(
        "\nTotal aligned segments: "
        f"{len(aligned)}"
    )


if __name__ == "__main__":
    main()