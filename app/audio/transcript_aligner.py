from dataclasses import dataclass


@dataclass
class AlignedSegment:
    start_time: float
    end_time: float
    speaker: str
    text: str


class TranscriptAligner:

    @staticmethod
    def _overlap(
        a_start: float,
        a_end: float,
        b_start: float,
        b_end: float,
    ) -> float:

        return max(
            0.0,
            min(a_end, b_end)
            - max(a_start, b_start),
        )

    def align(
        self,
        transcript_segments,
        diarization_segments,
    ) -> list[AlignedSegment]:

        if not transcript_segments:
            return []

        if not diarization_segments:
            raise ValueError(
                "No diarization segments available."
            )

        aligned = []

        for transcript in transcript_segments:

            best_speaker = None
            best_overlap = 0.0

            for diarization in diarization_segments:

                overlap = self._overlap(
                    transcript.start_time,
                    transcript.end_time,
                    diarization["start_time"],
                    diarization["end_time"],
                )

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = diarization[
                        "speaker"
                    ]

            # If there is no temporal overlap, use
            # the closest diarization segment.
            if best_speaker is None:

                midpoint = (
                    transcript.start_time
                    + transcript.end_time
                ) / 2

                closest = min(
                    diarization_segments,
                    key=lambda item: abs(
                        (
                            item["start_time"]
                            + item["end_time"]
                        ) / 2
                        - midpoint
                    ),
                )

                best_speaker = closest[
                    "speaker"
                ]

            aligned.append(
                AlignedSegment(
                    start_time=(
                        transcript.start_time
                    ),
                    end_time=(
                        transcript.end_time
                    ),
                    speaker=best_speaker,
                    text=transcript.text,
                )
            )

        return aligned


transcript_aligner = TranscriptAligner()