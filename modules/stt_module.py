import os
import tempfile
import whisper
import sounddevice as sd
import scipy.io.wavfile as wav

class SpeechToText:
    def __init__(self, model_name="base", duration=5, samplerate=16000):
        self.model = whisper.load_model(model_name)
        self.duration = duration
        self.samplerate = samplerate

    def record_and_transcribe(self) -> str:
        print("Recording audio for", self.duration, "seconds...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            audio = sd.rec(int(self.duration * self.samplerate), samplerate=self.samplerate, channels=1, dtype='int16')
            sd.wait()
            wav.write(tmpfile.name, self.samplerate, audio)
            print("Recording complete.")
            text = self.transcribe(tmpfile.name)
            os.unlink(tmpfile.name)
            return text

    def transcribe(self, audio_path: str) -> str:
        print("Transcribing...")
        result = self.model.transcribe(audio_path)
        print("Transcription complete.")
        return result["text"]
