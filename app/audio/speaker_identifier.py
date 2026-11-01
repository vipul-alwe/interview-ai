class SpeakerIdentifier:

    def identify(self, aligned_segments):
        if not aligned_segments:
            raise ValueError(
                "No aligned segments available."
            )

        speaker_duration = {}

        for segment in aligned_segments:
            duration = max(
                0.0,
                segment.end_time
                - segment.start_time,
            )

            speaker_duration[
                segment.speaker
            ] = (
                speaker_duration.get(
                    segment.speaker,
                    0.0,
                )
                + duration
            )

        if len(speaker_duration) < 2:
            raise ValueError(
                "Expected at least two speakers."
            )

        # In a normal interview the candidate has
        # substantially more speaking time than the
        # interviewer because interviewer speech is
        # mostly questions/feedback.
        candidate_speaker = max(
            speaker_duration,
            key=speaker_duration.get,
        )

        interviewer_speakers = [
            speaker
            for speaker in speaker_duration
            if speaker != candidate_speaker
        ]

        print(
            "[SPEAKER] Speaking durations:"
        )

        for speaker, duration in sorted(
            speaker_duration.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            print(
                f"[SPEAKER] {speaker}: "
                f"{duration:.2f}s"
            )

        print(
            "[SPEAKER] Candidate: "
            f"{candidate_speaker}"
        )

        print(
            "[SPEAKER] Interviewer: "
            f"{', '.join(interviewer_speakers)}"
        )

        labelled = []

        for segment in aligned_segments:

            if segment.speaker == candidate_speaker:
                speaker = "candidate"
            else:
                speaker = "interviewer"

            labelled.append(
                type(segment)(
                    start_time=segment.start_time,
                    end_time=segment.end_time,
                    speaker=speaker,
                    text=segment.text,
                )
            )

        return labelled


speaker_identifier = SpeakerIdentifier()