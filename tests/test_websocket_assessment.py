import asyncio
import wave

import numpy as np
import websockets

from app.core.interview_manager import manager


HOST = "127.0.0.1"
PORT = 8000


async def main():

    session = manager.create()

    interview_id = session.interview_id

    url = (
        f"ws://{HOST}:{PORT}"
        f"/ws/audio/{interview_id}"
    )

    print(
        f"Interview: {interview_id}"
    )

    with wave.open(
        "tests/data/test.wav",
        "rb",
    ) as wav:

        sample_rate = wav.getframerate()

        audio = np.frombuffer(
            wav.readframes(
                wav.getnframes()
            ),
            dtype=np.int16,
        )

    print(
        f"Audio: "
        f"{len(audio) / sample_rate:.2f}s"
    )

    async with websockets.connect(url) as websocket:

        print("WebSocket connected.")

        chunk_size = sample_rate * 2

        for i in range(
            0,
            len(audio),
            chunk_size,
        ):

            chunk = audio[
                i:i + chunk_size
            ].tobytes()

            await websocket.send(
                chunk
            )

            await asyncio.sleep(0.05)

        print(
            "Audio sent. "
            "Waiting for processing..."
        )

        await asyncio.sleep(8)

    print("\n=== SESSION RESULTS ===")

    print(
        f"Transcript segments: "
        f"{len(session.transcript)}"
    )

    print(
        f"Evidence: "
        f"{len(session.evidence)}"
    )

    print("\nCompetencies with evidence:")

    for competency_id, state in (
        session.competencies.items()
    ):

        if not state.evidence:
            continue

        print(
            f"\n{competency_id}"
        )

        print(
            f"  Evidence: "
            f"{len(state.evidence)}"
        )

        print(
            f"  Confidence: "
            f"{state.confidence:.2f}"
        )

        print(
            f"  Coverage: "
            f"{state.coverage:.2f}"
        )

        for evidence in state.evidence:

            print(
                f"  → {evidence.quote}"
            )


if __name__ == "__main__":
    asyncio.run(main())