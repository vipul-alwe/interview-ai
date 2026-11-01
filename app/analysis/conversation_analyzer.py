from app.llm.client import llm_client
from app.llm.parser import LLMParser
from app.utils.progress import StepProgress


class ConversationAnalyzer:

    WINDOW_SIZE = 8
    OVERLAP = 2

    def _build_prompt(
        self,
        segments,
    ) -> str:

        transcript = "\n".join(
            (
                f"[{i}] "
                f"{segment.start_time:.2f}-"
                f"{segment.end_time:.2f}: "
                f"{segment.text}"
            )
            for i, segment in enumerate(
                segments
            )
        )

        return f"""
You are identifying speakers in an interview transcript.

The transcript comes from one continuous recording.

For EVERY segment, classify only the speaker:

candidate
interviewer

Rules:

1. Use conversational context.
2. Interview questions are normally interviewer speech.
3. Detailed first-person career/project stories are normally
   candidate speech.
4. Short acknowledgements such as "right", "okay", "got it"
   should normally be interviewer speech when they interrupt
   a candidate answer.
5. Do not rewrite any text.
6. Do not omit segments.
7. Return exactly one classification for every supplied segment.
8. Preserve the segment index exactly.

Return ONLY JSON.

FORMAT:

{{
  "segments": [
    {{
      "index": 0,
      "speaker": "interviewer"
    }},
    {{
      "index": 1,
      "speaker": "candidate"
    }}
  ]
}}

TRANSCRIPT:

{transcript}
"""

    def _classify_window(
        self,
        segments,
    ) -> dict[int, str]:

        prompt = self._build_prompt(
            segments
        )

        raw = llm_client.generate_json(
            prompt=prompt,
            schema={
                "type": "object",
                "properties": {
                    "segments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "index": {
                                    "type": "integer"
                                },
                                "speaker": {
                                    "type": "string",
                                    "enum": [
                                        "candidate",
                                        "interviewer",
                                    ],
                                },
                            },
                            "required": [
                                "index",
                                "speaker",
                            ],
                        },
                    }
                },
                "required": [
                    "segments"
                ],
            },
        )

        data = LLMParser.parse_json(
            raw
        )

        result = {}

        for item in data.get(
            "segments",
            [],
        ):

            index = item.get(
                "index"
            )

            speaker = item.get(
                "speaker"
            )

            if speaker not in {
                "candidate",
                "interviewer",
            }:
                continue

            result[index] = speaker

        return result

    def _classify_segments(
        self,
        segments,
    ) -> list[str]:

        total = len(segments)

        if total == 0:
            return []

        votes = [
            {
                "candidate": 0,
                "interviewer": 0,
            }
            for _ in range(total)
        ]

        step = (
            self.WINDOW_SIZE
            - self.OVERLAP
        )

        windows = (
            total + step - 1
        ) // step

        progress = StepProgress(
            total=windows,
            label="Speaker classification",
        )

        start = 0
        window_number = 0

        while start < total:

            end = min(
                start
                + self.WINDOW_SIZE,
                total,
            )

            window = segments[
                start:end
            ]

            window_number += 1

            print(
                "[CONVERSATION] "
                f"Classifying window "
                f"{window_number}/{windows} "
                f"(segments "
                f"{start}-{end - 1})"
            )

            classifications = (
                self._classify_window(
                    window
                )
            )

            for index, speaker in (
                classifications.items()
            ):

                if (
                    0 <= index < total
                ):
                    votes[index][
                        speaker
                    ] += 1

            progress.update(
                current=window_number,
                message=(
                    f"segments "
                    f"{start}-{end - 1}"
                ),
            )

            start += step

        labels = []

        for index, vote in enumerate(
            votes
        ):

            candidate_votes = vote[
                "candidate"
            ]

            interviewer_votes = vote[
                "interviewer"
            ]

            if (
                candidate_votes == 0
                and interviewer_votes == 0
            ):

                if labels:
                    labels.append(
                        labels[-1]
                    )
                else:
                    labels.append(
                        "candidate"
                    )

            elif (
                candidate_votes
                > interviewer_votes
            ):

                labels.append(
                    "candidate"
                )

            else:

                labels.append(
                    "interviewer"
                )

        return labels

    def _build_turns(
        self,
        segments,
        speakers,
    ) -> list[dict]:

        if not segments:
            return []

        turns = []

        current_speaker = speakers[0]

        current_segments = [
            segments[0]
        ]

        for index in range(
            1,
            len(segments),
        ):

            speaker = speakers[index]

            if speaker == current_speaker:

                current_segments.append(
                    segments[index]
                )

                continue

            turns.append(
                self._make_turn(
                    current_segments,
                    current_speaker,
                )
            )

            current_speaker = speaker

            current_segments = [
                segments[index]
            ]

        turns.append(
            self._make_turn(
                current_segments,
                current_speaker,
            )
        )

        return turns

    def _make_turn(
        self,
        segments,
        speaker,
    ) -> dict:

        text = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        if speaker == "interviewer":

            turn_type = (
                "question"
                if "?" in text
                else "other"
            )

        else:

            turn_type = "answer"

        return {
            "start_time":
                segments[0].start_time,

            "end_time":
                segments[-1].end_time,

            "speaker":
                speaker,

            "type":
                turn_type,

            "text":
                text,

            "source_start_segment":
                segments[0].start_time,

            "source_end_segment":
                segments[-1].end_time,
        }

    def analyze(
        self,
        segments,
    ) -> dict:

        print(
            "[CONVERSATION] "
            f"Total transcript segments: "
            f"{len(segments)}"
        )

        speakers = (
            self._classify_segments(
                segments
            )
        )

        candidate_count = sum(
            speaker == "candidate"
            for speaker in speakers
        )

        interviewer_count = sum(
            speaker == "interviewer"
            for speaker in speakers
        )

        print(
            "[CONVERSATION] Candidate segments: "
            f"{candidate_count}"
        )

        print(
            "[CONVERSATION] Interviewer segments: "
            f"{interviewer_count}"
        )

        turns = self._build_turns(
            segments,
            speakers,
        )

        print(
            "[CONVERSATION] Final turns: "
            f"{len(turns)}"
        )

        print(
            "[CONVERSATION] Candidate turns: "
            f"{sum(t['speaker'] == 'candidate' for t in turns)}"
        )

        print(
            "[CONVERSATION] Interviewer turns: "
            f"{sum(t['speaker'] == 'interviewer' for t in turns)}"
        )

        return {
            "turns": turns,
            "segment_speakers": speakers,
        }


conversation_analyzer = ConversationAnalyzer()