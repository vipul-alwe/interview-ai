import re

from app.domain.transcript_segment import TranscriptSegment


FILLERS = {
    "um",
    "uh",
    "er",
    "ah",
}


class SpeechFeatureExtractor:

    def extract(
        self,
        segments: list[TranscriptSegment],
        candidate_speaker: str = "candidate",
    ) -> dict[str, float]:

        if not segments:
            return {}

        segments = sorted(
            segments,
            key=lambda segment: segment.start_time,
        )

        candidate_segments = [
            segment
            for segment in segments
            if segment.speaker == candidate_speaker
        ]

        if not candidate_segments:
            return {}

        total_words = 0
        filler_count = 0

        candidate_speech_duration = 0.0
        candidate_pauses = []
        response_latencies = []

        for index, segment in enumerate(candidate_segments):

            words = re.findall(
                r"\b[\w']+\b",
                segment.text.lower(),
            )

            total_words += len(words)

            filler_count += sum(
                1
                for word in words
                if word in FILLERS
            )

            candidate_speech_duration += (
                segment.end_time - segment.start_time
            )

            # Pause between consecutive candidate turns/segments.
            if index > 0:

                previous = candidate_segments[index - 1]

                pause = (
                    segment.start_time
                    - previous.end_time
                )

                if pause > 0:
                    candidate_pauses.append(pause)

            # Find the immediately preceding interviewer segment.
            previous_segments = [
                previous
                for previous in segments
                if (
                    previous.end_time <= segment.start_time
                    and previous.speaker != candidate_speaker
                )
            ]

            if previous_segments:

                previous = max(
                    previous_segments,
                    key=lambda item: item.end_time,
                )

                latency = (
                    segment.start_time
                    - previous.end_time
                )

                if latency >= 0:
                    response_latencies.append(latency)

        total_candidate_duration = (
            candidate_segments[-1].end_time
            - candidate_segments[0].start_time
        )

        speech_rate = (
            total_words
            / candidate_speech_duration
            * 60
            if candidate_speech_duration > 0
            else 0.0
        )

        filler_rate = (
            filler_count
            / total_words
            * 100
            if total_words > 0
            else 0.0
        )

        return {
            "word_count": float(total_words),

            "speech_duration_seconds": (
                candidate_speech_duration
            ),

            "total_duration_seconds": (
                total_candidate_duration
            ),

            "speech_rate_wpm": speech_rate,

            "filler_count": float(filler_count),

            "filler_rate_percent": filler_rate,

            "pause_count": float(
                len(candidate_pauses)
            ),

            "longest_pause_seconds": (
                max(candidate_pauses)
                if candidate_pauses
                else 0.0
            ),

            "average_pause_seconds": (
                sum(candidate_pauses)
                / len(candidate_pauses)
                if candidate_pauses
                else 0.0
            ),

            "response_latency_count": float(
                len(response_latencies)
            ),

            "average_response_latency_seconds": (
                sum(response_latencies)
                / len(response_latencies)
                if response_latencies
                else 0.0
            ),

            "longest_response_latency_seconds": (
                max(response_latencies)
                if response_latencies
                else 0.0
            ),
        }


speech_feature_extractor = SpeechFeatureExtractor()