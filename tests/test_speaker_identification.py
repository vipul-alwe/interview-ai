from pathlib import Path

from app.audio.transcription import transcriber
from app.audio.diarization import diarizer
from app.audio.transcript_aligner import (
    transcript_aligner,
)
from app.audio.speaker_identifier import (
    speaker_identifier,
)


AUDIO_PATH = Path(
    "temp_audio/interview.wav"
)


def main():

    print(
        "Transcribing..."
    )

    transcript = (
        transcriber.transcribe_file(
            AUDIO_PATH
        )
    )

    print(
        f"Transcript segments: "
        f"{len(transcript)}"
    )

    print(
        "\nDiarizing..."
    )

    diarization = diarizer.diarize(
        AUDIO_PATH,
        min_speakers=2,
        max_speakers=5,
    )

    print(
        "\nAligning..."
    )

    aligned = transcript_aligner.align(
        transcript,
        diarization,
    )

    print(
        f"Aligned segments: "
        f"{len(aligned)}"
    )

    print(
        "\nIdentifying speakers..."
    )

    labelled = speaker_identifier.identify(
        aligned
    )

    print(
        "\n" + "=" * 90
    )

    print(
        "LABELLED TRANSCRIPT"
    )

    print(
        "=" * 90
    )

    for segment in labelled:

        print(
            f"{segment.start_time:8.2f} - "
            f"{segment.end_time:8.2f} | "
            f"{segment.speaker:12} | "
            f"{segment.text}"
        )


if __name__ == "__main__":
    main()