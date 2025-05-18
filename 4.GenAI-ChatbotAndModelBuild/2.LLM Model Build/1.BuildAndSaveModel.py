import random
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer

import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, Activation
from tensorflow.keras.optimizers import RMSprop

# import the LSTM layer
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import Optimizer

text_df = pd.read_csv("fake_or_real_news.csv")
text = list(text_df.text.values)
joined_text = " ".join(text)

with open("joined_text.txt", "w") as f:
    f.write(joined_text)
    
partial_text = joined_text[:100000]  # Get the first 1000 characters

# Data pre processing i.e tokenization
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(partial_text)

# craete unique tokens
unique_tokens = np.unique(tokens)

# store with index
unique_tokens_index = {}
for i, token in enumerate(unique_tokens):
    unique_tokens_index[token] = i


n_words = 10
input_words = []
next_words = []

for i in range(len(tokens) - n_words):
    input_words.append(tokens[i:i + n_words])
    next_words.append(tokens[i + n_words])

# Split the data into training and testing
X = np.zeros((len(input_words), n_words, len(unique_tokens)), dtype=np.bool_)
Y = np.zeros((len(next_words), len(unique_tokens)), dtype=np.bool_)

for i, words in enumerate(input_words):
    for j, word in enumerate(words):
        X[i, j, unique_tokens_index[word]] = 1
    Y[i, unique_tokens_index[next_words[i]]] = 1


# Create the model
model = Sequential()

# Explain : LSTM is a type of recurrent neural network (RNN) that is capable of learning long-term dependencies. 
# It is particularly well-suited for sequence prediction problems, such as text generation.
model.add(LSTM(128, input_shape=(n_words, len(unique_tokens)), return_sequences=True))
model.add(LSTM(128))
model.add(Dense(len(unique_tokens)))
model.add(Activation('softmax'))
optimizer = RMSprop(learning_rate=0.01)

model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])

history = model.fit(X, Y, batch_size=128, epochs=10, shuffle=True).history
model.save("text_generator_model.h5")

print(Y)