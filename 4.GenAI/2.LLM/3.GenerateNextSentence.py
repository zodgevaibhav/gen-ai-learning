import random
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.optimizers import RMSprop

# Load the dataset containing news articles
# The dataset is expected to have a column named 'text' containing the news content
text_df = pd.read_csv("fake_or_real_news.csv")
text = list(text_df.text.values)

# Combine all the news articles into a single string
# This is done to create a large corpus of text for training the model
joined_text = " ".join(text)

# Save the combined text to a file for future reference or debugging
with open("joined_text.txt", "w", encoding="utf-8") as f:
    f.write(joined_text)

# Use only the first 1,000,000 characters of the text for training
# This is done to limit the size of the dataset for computational efficiency
partial_text = joined_text[:1000000]

# Tokenize the text into words using a regular expression tokenizer
# This removes punctuation and splits the text into individual words
tokenizer = RegexpTokenizer(r"\w+")
tokens = tokenizer.tokenize(partial_text.lower())  # Convert to lowercase for consistency
len(tokens)

# Get the unique tokens (vocabulary) from the tokenized text
# This helps in creating a mapping of words to indices for one-hot encoding
# One-hot encoding meaning each word is represented as a binary vector to represent its presence
# in the text
unique_tokens = np.unique(tokens)
unique_tokens

# Create a mapping of each unique token to a unique index
# This is required for one-hot encoding of the input and output
unique_token_index = {token: index for index, token in enumerate(unique_tokens)}
len(unique_token_index)

# Define the number of words to consider as input for predicting the next word
# This is a hyperparameter that can be tuned based on the dataset and model performance
n_words = 10
input_words = []  # List to store sequences of input words
next_word = []    # List to store the corresponding next word for each input sequence

# Create input-output pairs for training
# For each sequence of 'n_words', the next word is the target output
for i in range(len(tokens) - n_words):
    input_words.append(tokens[i:i + n_words])
    next_word.append(tokens[i + n_words])

# Initialize the input (X) and output (y) arrays for the model
# X is a 3D array where each sample is a one-hot encoded representation of 'n_words'
# y is a 2D array where each sample is a one-hot encoded representation of the next word
X = np.zeros((len(input_words), n_words, len(unique_tokens)), dtype=bool)  
y = np.zeros((len(next_word), len(unique_tokens)), dtype=bool)  

# Populate the input (X) and output (y) arrays with one-hot encoded values
for i, words in enumerate(input_words):
    for j, word in enumerate(words):
        X[i, j, unique_token_index[word]] = 1  # One-hot encode the input words
    y[i, unique_token_index[next_word[i]]] = 1  # One-hot encode the next word

# Define the model architecture
# The model uses two LSTM layers followed by a Dense layer with a softmax activation
# LSTM layers are used for their ability to capture sequential dependencies in text
model = Sequential()
model.add(LSTM(128, input_shape=(n_words, len(unique_tokens)), return_sequences=True))
model.add(LSTM(128))
model.add(Dense(len(unique_tokens)))
model.add(Activation("softmax"))

# Compile the model with categorical crossentropy loss and RMSprop optimizer
# Categorical crossentropy is used because the output is a probability distribution
optimizer = RMSprop(learning_rate=0.01)
model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

# Train the model on the input-output pairs
# The model learns to predict the next word given a sequence of 'n_words'
history = model.fit(X, y, batch_size=128, epochs=10, shuffle=True).history

# Save the trained model to a file for future use
model.save("text_gen_model2.h5")

# Load the model from the file (useful for inference or further training)
model = load_model("text_gen_model2.h5")

def predict_next_word(input_text, n_best):
    input_text = input_text.lower()
    X = np.zeros((1, n_words, len(unique_tokens)))
    for i, word in enumerate(input_text.split()):
        X[0, i, unique_token_index[word]] = 1
        
    predictions = model.predict(X)[0]
    print(f"predictions = {predictions}")
    return np.argpartition(predictions, -n_best)[-n_best:]

possible=predict_next_word("I will have to look in to this because I ", 5)
for idx in possible:
    print(unique_tokens[idx])

def generate_text(input_text, n_words, creativity=100):
    word_sequence = input_text.split()
    current = 0
    for _ in range(n_words):
        sub_sequence = " ".join(tokenizer.tokenize(" ".join(word_sequence).lower())[current:current+n_words])
        try:
            choice = unique_tokens[random.choice(predict_next_word(sub_sequence, creativity))]
        except:
            choice = random.choice(unique_tokens)
        word_sequence.append(choice)
        current += 1
    return " ".join(word_sequence)

print(generate_text("I will have to look in to this because I ", 100))