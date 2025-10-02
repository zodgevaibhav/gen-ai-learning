from transformers import pipeline
import IPython.display as ipd
from scipy.io.wavfile import write
import torch
import numpy as np

# Initialize pipeline
pipe = pipeline(
    "text-to-audio", model="facebook/musicgen-small", device="mps",torch_dtype=torch.float16
)  # or device=0 for CUDA

# Generate audio
data = pipe(
    "Hi, this is my first audio"
)  # returns dict with "samples" and "sampling_rate"

# Play audio
#ipd.display(ipd.Audio(data["audio"][0], rate=data["sampling_rate"]))

audio_int16 = np.int16(data["audio"][0] * 32767)

write("output.wav", data["sampling_rate"], audio_int16)


del pipe
torch.mps.empty_cache()
