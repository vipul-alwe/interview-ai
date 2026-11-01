import asyncio
import traceback
from datetime import datetime, timezone

from app.audio.segmenter import Segmenter
from app.audio.transcription import transcriber

from app.core.session import InterviewSession

from app.domain.response import Response

from app.engine.assessment_engine import (
    assessment_engine,
)

from app.engine.competency_state_engine import (
    competency_state_engine,
)

from app.engine.conversation_engine import (
    conversation_engine,
)

from app.engine.evidence_extractor import (
    evidence_extractor,
)


class AudioPipeline:

    def __init__(
        self,
        session: InterviewSession,
    ):
        self.session = session

        self.segmenter = Segmenter()

        self.analysis_queue = asyncio.Queue()
        self.result_queue = asyncio.Queue()

        self.worker_task = asyncio.create_task(
            self._analysis_worker()
        )

    async def process_chunk(
        self,
        audio_chunk: bytes,
    ):
        print(
            f"Received audio chunk: "
            f"{len(audio_chunk)} bytes"
        )

        completed_segments = (
            self.segmenter.process_chunk(
                audio_chunk
            )
        )

        for audio, audio_offset in completed_segments:

            loop = asyncio.get_running_loop()

            transcript_segments = (
                await loop.run_in_executor(
                    None,
                    transcriber.transcribe,
                    audio,
                    audio_offset,
                    "candidate",
                )
            )

            if not transcript_segments:
                continue

            transcript = " ".join(
                segment.text
                for segment in transcript_segments
            ).strip()

            if not transcript:
                continue

            now = datetime.now(timezone.utc)

            sample_rate = getattr(
                self.segmenter,
                "SAMPLE_RATE",
                16000,
            )

            duration = (
                len(audio) / sample_rate
            )

            response = Response(
                question_id=(
                    self.session.current_question.question_id
                    if self.session.current_question
                    else ""
                ),
                transcript=transcript,
                segments=transcript_segments,
                started_at=now,
                ended_at=now,
                duration=duration,
            )

            self.session.transcript.append(
                transcript
            )

            await self.analysis_queue.put(
                response
            )

            print(
                "[PIPELINE] Response queued "
                "for analysis."
            )

    async def _analysis_worker(self):

        while True:

            response = (
                await self.analysis_queue.get()
            )

            try:

                print(
                    "[ANALYSIS] Processing response:"
                )

                print(
                    f"[ANALYSIS] "
                    f"{response.transcript}"
                )

                # ----------------------------------------
                # 1. Extract evidence
                # ----------------------------------------

                evidence = await (
                    evidence_extractor.extract(
                        response=response,
                    )
                )

                self.session.evidence.extend(
                    evidence
                )

                print(
                    "[ANALYSIS] Evidence extracted: "
                    f"{len(evidence)}"
                )

                # ----------------------------------------
                # 2. Update competency states
                # ----------------------------------------

                competency_state_engine.apply(
                    states=self.session.competencies,
                    evidence=evidence,
                )

                affected_competencies = {
                    item.competency_id
                    for item in evidence
                }

                print(
                    "[ANALYSIS] Affected competencies: "
                    f"{len(affected_competencies)}"
                )

                # ----------------------------------------
                # 3. Assess affected competencies
                # ----------------------------------------

                for competency_id in (
                    affected_competencies
                ):

                    state = (
                        self.session.competencies.get(
                            competency_id
                        )
                    )

                    if state is None:
                        print(
                            "[ASSESSMENT] Skipping "
                            f"{competency_id}: "
                            "state not found."
                        )
                        continue

                    competency = None

                    try:
                        from app.registry.competency_registry import (
                            competency_registry,
                        )

                        competency = (
                            competency_registry.get(
                                competency_id
                            )
                        )

                        if competency is None:
                            raise ValueError(
                                "Competency not found in registry."
                            )

                        print(
                            "[ASSESSMENT] Competency type: "
                            f"{type(competency).__name__}"
                        )

                        print(
                            "[ASSESSMENT] Competency ID: "
                            f"{competency.id}"
                        )

                        print(
                            "[ASSESSMENT] Has indicators: "
                            f"{hasattr(competency, 'indicators')}"
                        )

                    except Exception:
                        print(
                            "[ASSESSMENT] Registry inspection failed:"
                        )
                        traceback.print_exc()

                    print(
                        "[ASSESSMENT] Assessing "
                        f"{competency_id}"
                    )

                    assessment_engine.assess(
                        competency_id=competency_id,
                        state=state,
                    )

                # ----------------------------------------
                # 4. Update conversation context
                # ----------------------------------------

                self.session.context.last_response = (
                    response.transcript
                )

                self.session.context.turn_count += 1

                # ----------------------------------------
                # 5. Generate dynamic next question
                # ----------------------------------------

                next_question = (
                    conversation_engine.generate(
                        self.session
                    )
                )

                print(
                    "[CONVERSATION] Next competency: "
                    f"{next_question.competency_id}"
                )

                print(
                    "[CONVERSATION] Next question: "
                    f"{next_question.question}"
                )

                # ----------------------------------------
                # 6. Build live result
                # ----------------------------------------

                result = {
                    "type": "analysis",
                    "response_id": response.id,
                    "question_id": response.question_id,
                    "transcript": response.transcript,
                    "evidence": [
                        item.model_dump(
                            mode="json"
                        )
                        for item in evidence
                    ],
                    "competencies": {
                        competency_id: state.model_dump(
                            mode="json"
                        )
                        for (
                            competency_id,
                            state,
                        ) in self.session.competencies.items()
                    },
                    "next_question": (
                        next_question.model_dump(
                            mode="json"
                        )
                    ),
                }

                await self.result_queue.put(
                    result
                )

                print(
                    "[ANALYSIS] Analysis complete."
                )

            except Exception as exc:

                print(
                    "[ANALYSIS] ERROR: "
                    f"{type(exc).__name__}: {exc}"
                )

                print(
                    "[ANALYSIS] FULL TRACEBACK:"
                )

                traceback.print_exc()

                await self.result_queue.put(
                    {
                        "type": "error",
                        "message": str(exc),
                        "exception_type": (
                            type(exc).__name__
                        ),
                    }
                )

            finally:

                self.analysis_queue.task_done()

    async def get_result(self):

        return await self.result_queue.get()

    async def close(self):

        self.worker_task.cancel()

        try:
            await self.worker_task

        except asyncio.CancelledError:
            pass
