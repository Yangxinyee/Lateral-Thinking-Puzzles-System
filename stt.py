import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

model = whisper.load_model("base")

DURATION = 5 
SAMPLERATE = 16000  # whisper works best with 16kHz

def record_audio(filename="temp.wav"):
    print("Recording...")
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, SAMPLERATE, audio)
    print("Recording complete.")
    return filename

def transcribe_audio(audio_path):
    print("Transcribing...")
    result = model.transcribe(audio_path)
    print("Transcription complete.\n")
    return result["text"]

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio_file = record_audio(tmpfile.name)
        text = transcribe_audio(audio_file)
        print(f"Transcribed Text:\n{text}")
        os.unlink(tmpfile.name)