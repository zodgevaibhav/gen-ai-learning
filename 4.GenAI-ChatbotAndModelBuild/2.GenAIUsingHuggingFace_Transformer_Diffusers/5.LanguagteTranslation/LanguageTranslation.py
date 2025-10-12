from transformers import pipeline, logging

logging.set_verbosity_error()


translator = pipeline(
    "translation_en_to_marathi", 
    model='Helsinki-NLP/opus-mt-en-mr', 
    device=0
    )  # use device="mps" for Apple, 0 for CUDA GPU, -1 for CPU

texts = "I love programming in Python."

translation = translator(texts, max_length=100)
print("English:", texts)
print("Marathi:", translation[0]['translation_text'])


