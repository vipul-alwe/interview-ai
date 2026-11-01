from pathlib import Path

import soundfile as sf
from faster_whisper import WhisperModel

from app.domain.transcript_segment import (
    TranscriptSegment,
)
from app.utils.progress import (
    ProgressTracker,
)


class Transcriber:

    def __init__(self):

        print(
            "[TRANSCRIPTION] Loading Whisper model..."
        )

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )

        print(
            "[TRANSCRIPTION] Whisper model loaded."
        )

    def transcribe(
        self,
        audio,
        audio_offset: float = 0.0,
        speaker: str = "unknown",
        duration: float | None = None,
    ) -> list[TranscriptSegment]:

        tracker = ProgressTracker(
            "Whisper transcription"
        )

        tracker.start()

        try:

            segments, _ = (
                self.model.transcribe(
                    audio,
                    language="en",
                    vad_filter=True,
                    vad_parameters={
                        "min_silence_duration_ms": 500,
                    },
                )
            )

            transcript_segments = []

            last_reported_second = -1

            for segment in segments:

                text = segment.text.strip()

                if not text:
                    continue

                transcript_segments.append(
                    TranscriptSegment(
                        speaker=speaker,
                        start_time=(
                            audio_offset
                            + segment.start
                        ),
                        end_time=(
                            audio_offset
                            + segment.end
                        ),
                        text=text,
                    )
                )

                # --------------------------------------
                # Real progress based on audio position
                # --------------------------------------

                if duration:

                    current_second = int(
                        segment.end
                    )

                    if (
                        current_second
                        > last_reported_second
                    ):

                        last_reported_second = (
                            current_second
                        )

                        percentage = min(
                            100.0,
                            (
                                segment.end
                                / duration
                                * 100
                            ),
                        )

                        print(
                            "[TRANSCRIPTION] "
                            f"{percentage:5.1f}% "
                            f"({segment.end:.1f}s/"
                            f"{duration:.1f}s) "
                            f"| segments: "
                            f"{len(transcript_segments)}"
                        )

            tracker.stop(
                message=(
                    f"{len(transcript_segments)} "
                    "segments"
                )
            )

            return transcript_segments

        except Exception:

            tracker.stop(
                message="failed"
            )

            raise

    def transcribe_file(
        self,
        audio_path: str | Path,
    ) -> list[TranscriptSegment]:

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        # ------------------------------------------
        # Determine audio duration
        # ------------------------------------------

        duration = None

        try:

            info = sf.info(
                str(audio_path)
            )

            duration = (
                info.frames
                / info.samplerate
            )

        except Exception:

            print(
                "[TRANSCRIPTION] "
                "Could not determine audio duration."
            )

        print(
            "[TRANSCRIPTION] Audio: "
            f"{audio_path}"
        )

        if duration:
            print(
                "[TRANSCRIPTION] Duration: "
                f"{duration:.1f}s"
            )

        return self.transcribe(
            audio=str(audio_path),
            audio_offset=0.0,
            speaker="unknown",
            duration=duration,
        )


transcriber = Transcriber()