from transformers import pipeline, logging
import tkinter as tk
from tkinter import messagebox

logging.set_verbosity_error()

# root = tk.Tk()

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
texts = "I love programming in Python."

translation = translator(texts, max_length=100)
print("English:", texts)
print("Marathi:", translation[0]['translation_text'])


