import wave

import numpy as np

from app.audio.segmenter import Segmenter
from app.audio.transcription import transcriber


def main():

    with wave.open("tests/data/test.wav", "rb") as f:
        audio = np.frombuffer(
            f.readframes(f.getnframes()),
            dtype=np.int16,
        )

    # Add 3 seconds of silence so the Segmenter
    # can close the speech segment.
    audio = np.concatenate(
        (
            audio,
            np.zeros(3 * 16000, dtype=np.int16),
        )
    )

    segmenter = Segmenter()

    # 1 second of mono 16 kHz int16 PCM.
    chunk_size = 16000 * 2

    completed = []

    for i in range(0, len(audio), chunk_size):

        chunk = audio[i:i + chunk_size]

        completed.extend(
            segmenter.process_chunk(
                chunk.tobytes()
            )
        )

    print(f"Segments: {len(completed)}")

    for i, (segment, audio_offset) in enumerate(
        completed
    ):

        print(
            f"\nSegment {i}:"
            f"\n  type: {type(segment)}"
            f"\n  shape: {segment.shape}"
            f"\n  dtype: {segment.dtype}"
            f"\n  samples: {segment.size}"
            f"\n  duration: "
            f"{len(segment) / 16000:.2f}s"
            f"\n  offset: {audio_offset:.2f}s"
        )

        if segment.size == 0:
            print("Skipping empty segment.")
            continue

        result = transcriber.transcribe(
            segment,
            audio_offset=audio_offset,
        )

        print("\nTranscript:")

        for item in result:
            print(
                f"[{item.start_time:.2f}s - "
                f"{item.end_time:.2f}s] "
                f"{item.text}"
            )


if __name__ == "__main__":
    main()