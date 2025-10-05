import sounddevice as sound_device
import numpy as np
import torch
from transformers import pipeline, logging

logging.set_verbosity_error()

# --- Load Whisper model ---
device = "cuda" if torch.cuda.is_available() else "mps"
model_pipeline = pipeline(model="openai/whisper-medium", device=device)

# --- Audio settings ---
sample_rate = 16000  # Whisper expects 16kHz
duration = 5         # seconds per recording

print("Speak now (Ctrl+C to stop)...")

try:
    while True:
        print("\nListening...")
        audio = sound_device.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sound_device.wait()
        audio_data = np.squeeze(audio) # Convert to mono numpy array

        print("Transcribing...")
        result = model_pipeline({"array": audio_data, "sampling_rate": sample_rate})

        print("You said:", result["text"])

except KeyboardInterrupt:
    print("\n Stopped.")
