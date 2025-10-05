from transformers import pipeline, logging

logging.set_verbosity_error()

# ---------------------------
# Step 1: Define model for Marathi
# ---------------------------
MODELS = {
    'marathi': 'Helsinki-NLP/opus-mt-en-mr'
}

translator = pipeline("translation_en_to_marathi", model=MODELS['marathi'], device=0)  # use device="mps" for Apple, 0 for CUDA GPU, -1 for CPU

# ---------------------------
# Step 2: Translate sentences
# ---------------------------
texts = [
    "Hello, how are you?",
    "I love programming in Python.",
    "The weather today is very pleasant."
]

for text in texts:
    translation = translator(text, max_length=100)
    print("English:", text)
    print("Marathi:", translation[0]['translation_text'])
    print()
