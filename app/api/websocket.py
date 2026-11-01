import asyncio

from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
)

from app.core.interview_manager import manager
from app.services.audio_pipeline import AudioPipeline


router = APIRouter()


@router.websocket("/audio/{interview_id}")
async def audio_stream(
    websocket: WebSocket,
    interview_id: str,
):
    await websocket.accept()

    print(
        f"WebSocket connection received: "
        f"{interview_id}"
    )

    session = manager.get(interview_id)

    if session is None:
        print(
            f"Invalid interview ID: "
            f"{interview_id}"
        )

        await websocket.close(
            code=1008,
            reason="Invalid interview ID",
        )

        return

    pipeline = AudioPipeline(
        session=session
    )

    print(
        f"Audio pipeline ready: "
        f"{interview_id}"
    )

    async def receive_audio():
        while True:

            message = (
                await websocket.receive()
            )

            message_type = message.get(
                "type"
            )

            if message_type == "websocket.disconnect":
                raise WebSocketDisconnect

            audio_chunk = message.get(
                "bytes"
            )

            if audio_chunk is None:
                continue

            await pipeline.process_chunk(
                audio_chunk
            )

    async def send_results():
        while True:

            result = await pipeline.get_result()

            print(
                "[WS] Sending analysis."
            )

            await websocket.send_json(
                result
            )

    receiver_task = asyncio.create_task(
        receive_audio()
    )

    sender_task = asyncio.create_task(
        send_results()
    )

    try:

        done, pending = await asyncio.wait(
            [
                receiver_task,
                sender_task,
            ],
            return_when=asyncio.FIRST_EXCEPTION,
        )

        for task in done:

            exception = task.exception()

            if exception is not None:

                if isinstance(
                    exception,
                    WebSocketDisconnect,
                ):
                    raise exception

                raise exception

    except WebSocketDisconnect:

        print(
            f"Audio client disconnected: "
            f"{interview_id}"
        )

    except Exception as exc:

        print(
            "[WS] ERROR: "
            f"{type(exc).__name__}: {exc}"
        )

    finally:

        receiver_task.cancel()
        sender_task.cancel()

        await asyncio.gather(
            receiver_task,
            sender_task,
            return_exceptions=True,
        )

        await pipeline.close()

        print(
            f"[WS] Audio pipeline closed: "
            f"{interview_id}"
        )