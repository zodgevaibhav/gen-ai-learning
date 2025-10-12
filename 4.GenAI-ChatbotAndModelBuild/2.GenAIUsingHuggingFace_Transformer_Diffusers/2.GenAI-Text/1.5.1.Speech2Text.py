from transformers import pipeline, logging

logging.set_verbosity_error()

generator = pipeline(
    model="openai/whisper-medium"
    )
# sample audio files https://audio-samples.github.io/#section-1
audio_file = "mlk.flac"

text = generator(audio_file)

print(text['text'])

