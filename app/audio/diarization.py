import os
from pathlib import Path

import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline

from app.utils.progress import ProgressTracker


load_dotenv()


class Diarizer:

    def __init__(self):

        token = os.getenv("HF_TOKEN")

        if not token:
            raise RuntimeError(
                "HF_TOKEN environment variable is not set."
            )

        print(
            "[DIARIZATION] Loading speaker "
            "diarization model..."
        )

        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            token=token,
        )

        # ------------------------------------------
        # Select Apple Silicon GPU when available
        # ------------------------------------------

        if torch.backends.mps.is_available():

            self.device = torch.device("mps")

        else:

            self.device = torch.device("cpu")

        print(
            "[DIARIZATION] Device: "
            f"{self.device}"
        )

        self.pipeline.to(self.device)

        print(
            "[DIARIZATION] Model loaded."
        )

    def diarize(
        self,
        audio_path: str | Path,
        min_speakers: int = 2,
        max_speakers: int = 5,
    ):

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        print(
            "[DIARIZATION] Processing: "
            f"{audio_path}"
        )

        tracker = ProgressTracker(
            "Speaker diarization"
        )

        tracker.start()

        try:

            output = self.pipeline(
                str(audio_path),
                min_speakers=min_speakers,
                max_speakers=max_speakers,
            )

            segments = []

            # pyannote.audio 4.x:
            # (turn, speaker)

            for turn, speaker in (
                output.speaker_diarization
            ):

                segments.append(
                    {
                        "start_time": float(
                            turn.start
                        ),
                        "end_time": float(
                            turn.end
                        ),
                        "speaker": str(
                            speaker
                        ),
                    }
                )

            speakers = sorted(
                {
                    segment["speaker"]
                    for segment in segments
                }
            )

            tracker.stop(
                message=(
                    f"{len(speakers)} speakers, "
                    f"{len(segments)} segments"
                )
            )

            print(
                "[DIARIZATION] Speakers detected: "
                f"{len(speakers)}"
            )

            for speaker in speakers:

                print(
                    f"[DIARIZATION] {speaker}"
                )

            return segments

        except Exception:

            tracker.stop(
                message="failed"
            )

            raise


diarizer = Diarizer()