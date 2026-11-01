import asyncio
import json
import urllib.request
import wave

import websockets


BASE_URL = "http://127.0.0.1:8000"


def create_interview() -> str:

    request = urllib.request.Request(
        f"{BASE_URL}/interview/start",
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(
            response.read().decode("utf-8")
        )

    interview_id = data["interview_id"]

    print(
        f"Created interview: {interview_id}"
    )

    return interview_id


async def receive_messages(websocket):

    try:

        while True:

            message = await websocket.recv()

            print("\n" + "=" * 70)
            print("RAW SERVER RESPONSE")
            print("=" * 70)
            print(message)
            print("=" * 70)

    except websockets.ConnectionClosed:

        print(
            "\nWebSocket receiver closed."
        )


async def main():

    interview_id = create_interview()

    websocket_url = (
        f"ws://127.0.0.1:8000"
        f"/ws/audio/{interview_id}"
    )

    with wave.open(
        "tests/data/test.wav",
        "rb",
    ) as wav:

        audio = wav.readframes(
            wav.getnframes()
        )

    # Add 3 seconds of silence so the
    # speech segment is finalized by VAD.
    audio += b"\x00\x00" * (
        3 * 16000
    )

    chunk_size = 16000 * 2

    async with websockets.connect(
        websocket_url
    ) as websocket:

        print(
            "WebSocket connected."
        )

        receiver_task = asyncio.create_task(
            receive_messages(websocket)
        )

        try:

            for i in range(
                0,
                len(audio),
                chunk_size,
            ):

                chunk = audio[
                    i:i + chunk_size
                ]

                await websocket.send(
                    chunk
                )

                print(
                    f"Sent chunk "
                    f"{i // chunk_size + 1}"
                )

                await asyncio.sleep(
                    0.05
                )

            print(
                "\nAll audio sent."
            )

            # Allow enough time for:
            # transcription
            # evidence extraction
            # competency analysis
            await asyncio.sleep(20)

        finally:

            receiver_task.cancel()

            try:
                await receiver_task
            except asyncio.CancelledError:
                pass


if __name__ == "__main__":
    asyncio.run(main())