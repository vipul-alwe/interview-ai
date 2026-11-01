import numpy as np

from app.audio.vad import vad


class Segmenter:

    SAMPLE_RATE = 16000
    WINDOW_SIZE = SAMPLE_RATE
    SILENCE_WINDOWS_TO_END = 2

    def __init__(self):

        self.processing_buffer = np.array(
            [],
            dtype=np.float32,
        )

        self.speech_buffer = np.array(
            [],
            dtype=np.float32,
        )

        self.speech_active = False
        self.silence_counter = 0

        self.total_samples_processed = 0
        self.speech_start_sample = 0

    def process_chunk(
        self,
        audio_chunk: bytes,
    ):

        chunk = (
            np.frombuffer(
                audio_chunk,
                dtype=np.int16,
            )
            .astype(np.float32)
            / 32768.0
        )

        self.processing_buffer = np.concatenate(
            (
                self.processing_buffer,
                chunk,
            )
        )

        completed_segments = []

        while len(self.processing_buffer) >= self.WINDOW_SIZE:

            window_start_sample = (
                self.total_samples_processed
            )

            window = self.processing_buffer[
                : self.WINDOW_SIZE
            ]

            self.processing_buffer = (
                self.processing_buffer[
                    self.WINDOW_SIZE:
                ]
            )

            self.total_samples_processed += (
                self.WINDOW_SIZE
            )

            speech = vad.detect(window)

            if speech:

                if not self.speech_active:

                    self.speech_active = True

                    self.speech_buffer = (
                        np.array(
                            [],
                            dtype=np.float32,
                        )
                    )

                    self.speech_start_sample = (
                        window_start_sample
                    )

                self.silence_counter = 0

                self.speech_buffer = np.concatenate(
                    (
                        self.speech_buffer,
                        window,
                    )
                )

            elif self.speech_active:

                self.silence_counter += 1

                self.speech_buffer = np.concatenate(
                    (
                        self.speech_buffer,
                        window,
                    )
                )

                if (
                    self.silence_counter
                    >= self.SILENCE_WINDOWS_TO_END
                ):

                    completed_segments.append(
                        (
                            self.speech_buffer.copy(),
                            (
                                self.speech_start_sample
                                / self.SAMPLE_RATE
                            ),
                        )
                    )

                    self.speech_buffer = (
                        np.array(
                            [],
                            dtype=np.float32,
                        )
                    )

                    self.speech_active = False
                    self.silence_counter = 0

        return completed_segments


segmenter = Segmenter()