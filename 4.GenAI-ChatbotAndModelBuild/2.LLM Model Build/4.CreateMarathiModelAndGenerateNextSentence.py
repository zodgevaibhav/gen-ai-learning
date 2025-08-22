import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
import pickle

# -----------------------------
# Step 1: Load corpus from CSV
# -----------------------------
# Assume CSV has a column named "text" with Sanskrit sentences
corpus = pd.read_csv("case_paper.csv")  
texts = corpus["detailed_diagnosis_chikitsa"].astype(str).tolist()

# -----------------------------
# Step 2: Tokenize the text
# -----------------------------
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
total_words = len(tokenizer.word_index) + 1

print("Unique words:", total_words)

# -----------------------------
# Step 3: Create input sequences
# -----------------------------
input_sequences = []

for line in texts:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')

# Features (X) and labels (y)
X, y = input_sequences[:,:-1], input_sequences[:,-1]

# One-hot encode y
y = np.eye(total_words)[y]

# -----------------------------
# Step 4: Define the model
# -----------------------------
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# -----------------------------
# Step 5: Train the model
# -----------------------------
history = model.fit(X, y, epochs=50, verbose=1)

# Save the trained model to a file for future use
model.save("text_gen_model2.h5")

# Save the tokenizer
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)


# Load the model from the file (useful for inference or further training)
model = load_model("text_gen_model2.h5")

# -----------------------------
# Step 6: Generate text
# -----------------------------
def predict_next_word(seed_text, next_words=5):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list, verbose=0), axis=-1)
        
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                seed_text += " " + word
                break
    return seed_text

# Example usage:
print(predict_next_word("पित्त", next_words=5))
