from silero_vad import load_silero_vad, get_speech_timestamps


class VoiceActivityDetector:
    def __init__(self):
        self.model = load_silero_vad()

    def detect(self, audio, sample_rate=16000):
        return get_speech_timestamps(
            audio,
            self.model,
            sampling_rate=sample_rate
        )


vad = VoiceActivityDetector()