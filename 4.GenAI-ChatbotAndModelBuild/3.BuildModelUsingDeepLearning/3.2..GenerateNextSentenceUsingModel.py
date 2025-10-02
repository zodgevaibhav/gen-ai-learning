import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# -----------------------------
# 1. Load the saved model
# -----------------------------
model = load_model("text_gen_model2.h5")

# -----------------------------
# 2. Load tokenizer
# -----------------------------
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# -----------------------------
# 3. Load corpus (for reference, optional)
# -----------------------------
# df = pd.read_csv("corpus.csv")
# corpus = df["text"].tolist()

# -----------------------------
# 4. Function to predict next word
# -----------------------------
def predict_next_word(model, tokenizer, text_sequence, max_sequence_len=10):
    """Predict the next word for a given text sequence"""
    # Convert input text to sequence
    token_list = tokenizer.texts_to_sequences([text_sequence])[0]
    
    # Pad the sequence
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    
    # Predict probabilities
    predicted_probs = model.predict(token_list, verbose=0)
    predicted_index = np.argmax(predicted_probs, axis=-1)[0]
    
    # Convert index back to word
    for word, index in tokenizer.word_index.items():
        if index == predicted_index:
            return word
    return None

# -----------------------------
# 5. Try predictions
# -----------------------------
input_text = "पित्तघ्न"
next_word = predict_next_word(model, tokenizer, input_text)
next_word = next_word+" "+predict_next_word(model, tokenizer, next_word  )
print(f"{input_text} {next_word}")
