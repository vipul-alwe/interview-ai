import asyncio

import sounddevice as sd
import websockets

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 1024

WS_URL = "ws://127.0.0.1:8000/ws/audio"


async def stream():
    async with websockets.connect(WS_URL) as websocket:

        def callback(indata, frames, time, status):
            if status:
                print(status)

            asyncio.run_coroutine_threadsafe(
                websocket.send(indata.copy().tobytes()),
                loop
            )

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=BLOCK_SIZE,
            callback=callback,
        ):
            print("Streaming microphone...")
            await asyncio.Future()


loop = asyncio.get_event_loop()
loop.run_until_complete(stream())