import wave
import numpy as np

from app.audio.vad import vad
from app.audio.segmenter import Segmenter


def main():

    with wave.open("tests/data/test.wav", "rb") as f:
        audio = np.frombuffer(
            f.readframes(f.getnframes()),
            dtype=np.int16,
        )

    # Add 3 seconds of silence.
    audio = np.concatenate(
        (
            audio,
            np.zeros(3 * 16000, dtype=np.int16),
        )
    )

    segmenter = Segmenter()

    chunk_size = 16000 * 2  # 1 second of int16 PCM

    for i in range(0, len(audio), chunk_size):

        chunk = audio[i:i + chunk_size]

        window = (
            np.frombuffer(chunk, dtype=np.int16)
            .astype(np.float32)
            / 32768.0
        )

        vad_result = vad.detect(window)

        segments = segmenter.process_chunk(
            chunk
        )

        print(
            f"Window {i // chunk_size}: "
            f"VAD={bool(vad_result)}, "
            f"timestamps={vad_result}, "
            f"completed_segments={len(segments)}"
        )


if __name__ == "__main__":
    main()