from pathlib import Path

from app.audio.transcription import transcriber
from app.audio.diarization import diarizer
from app.audio.transcript_aligner import transcript_aligner
from app.audio.speaker_identifier import speaker_identifier
from app.analysis.interview_analyzer import interview_analyzer


AUDIO_PATH = Path("temp_audio/interview.wav")


def main():

    print("Audio file:", AUDIO_PATH)

    # ==================================================
    # PASS 0 — TRANSCRIPTION
    # ==================================================

    print("\nTranscribing complete interview...")

    transcript_segments = (
        transcriber.transcribe_file(
            AUDIO_PATH
        )
    )

    print(
        "Transcript segments:",
        len(transcript_segments),
    )

    # ==================================================
    # PASS 0.5 — DIARIZATION
    # ==================================================

    print("\nRunning speaker diarization...")

    diarization_segments = diarizer.diarize(
        AUDIO_PATH,
        min_speakers=2,
        max_speakers=5,
    )

    # ==================================================
    # PASS 0.75 — ALIGNMENT
    # ==================================================

    print("\nAligning transcript with speakers...")

    aligned_segments = (
        transcript_aligner.align(
            transcript_segments,
            diarization_segments,
        )
    )

    print(
        "Aligned segments:",
        len(aligned_segments),
    )

    # ==================================================
    # PASS 0.9 — SPEAKER IDENTIFICATION
    # ==================================================

    print("\nIdentifying candidate speaker...")

    labelled_segments = (
        speaker_identifier.identify(
            aligned_segments
        )
    )

    candidate_count = sum(
        1
        for segment in labelled_segments
        if segment.speaker == "candidate"
    )

    interviewer_count = sum(
        1
        for segment in labelled_segments
        if segment.speaker == "interviewer"
    )

    print(
        "Candidate segments:",
        candidate_count,
    )

    print(
        "Interviewer segments:",
        interviewer_count,
    )

    # ==================================================
    # FINAL ANALYSIS
    # ==================================================

    print("\nRunning full interview analysis...")

    result = interview_analyzer.analyze(
        labelled_segments
    )

    # ==================================================
    # RESULTS
    # ==================================================

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

    competencies = result[
        "competencies"
    ].get(
        "competencies",
        [],
    )

    print(
        "\nCompetencies assessed:",
        len(competencies),
    )

    for competency in competencies:

        print(
            f"\n{competency['competency_id']}"
        )

        print(
            "Rating:",
            competency["rating"],
        )

        print(
            "Confidence:",
            competency["confidence"],
        )

        print(
            "Evidence:",
            competency["supporting_evidence"],
        )

        print(
            "Rationale:",
            competency["rationale"],
        )


if __name__ == "__main__":
    main()