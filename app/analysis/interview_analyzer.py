import time

from app.analysis.evidence_analyzer import (
    evidence_analyzer,
)

from app.analysis.competency_analyzer import (
    competency_analyzer,
)

from app.utils.progress import (
    ProgressTracker,
)


class InterviewAnalyzer:

    def analyze(
        self,
        segments,
    ) -> dict:

        if not segments:
            raise ValueError(
                "No aligned transcript segments available."
            )

        overall = ProgressTracker(
            "Full interview analysis",
            interval=10.0,
        )

        overall.start()

        try:

            # ==================================================
            # PASS 1
            # ==================================================

            print(
                "\n"
                "[PASS 1/3] "
                "Preparing candidate transcript..."
            )

            candidate_segments = [
                segment
                for segment in segments
                if getattr(
                    segment,
                    "speaker",
                    None,
                ) == "candidate"
            ]

            print(
                "[PASS 1/3] Candidate segments: "
                f"{len(candidate_segments)}"
            )

            if not candidate_segments:
                raise ValueError(
                    "No candidate segments found."
                )

            # ==================================================
            # PASS 2
            # ==================================================

            print(
                "\n"
                "[PASS 2/3] "
                "Extracting behavioral evidence..."
            )

            evidence = (
                evidence_analyzer.analyze(
                    candidate_segments
                )
            )

            behavioral_atoms = (
                evidence.get(
                    "behavioral_atoms",
                    [],
                )
            )

            print(
                "[PASS 2/3] Behavioral atoms: "
                f"{len(behavioral_atoms)}"
            )

            if not behavioral_atoms:
                raise ValueError(
                    "No behavioral evidence atoms extracted."
                )

            # ==================================================
            # PASS 3
            # ==================================================

            print(
                "\n"
                "[PASS 3/3] "
                "Assessing competencies..."
            )

            competency_results = (
                competency_analyzer.analyze(
                    behavioral_atoms
                )
            )

            competencies = (
                competency_results.get(
                    "competencies",
                    [],
                )
            )

            print(
                "[PASS 3/3] Competencies assessed: "
                f"{len(competencies)}"
            )

            overall.stop(
                message=(
                    f"{len(behavioral_atoms)} atoms, "
                    f"{len(competencies)} competencies"
                )
            )

            return {
                "candidate_segments":
                    candidate_segments,

                "evidence":
                    evidence,

                "competencies":
                    competency_results,
            }

        except Exception:

            overall.stop(
                message="failed"
            )

            raise


interview_analyzer = InterviewAnalyzer()