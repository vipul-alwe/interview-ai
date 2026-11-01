import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
DURATION = 5

print("Recording...")
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32"
)

sd.wait()

sf.write("temp_audio/test.wav", audio, SAMPLE_RATE)

print("Saved to temp_audio/test.wav")