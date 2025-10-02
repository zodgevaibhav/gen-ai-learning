# This code creates a deep learning model for text generation using news data. 
# It processes text data and trains an LSTM neural network to predict 
# the next word in a sequence.
    

import random  # Import random module for generating random numbers
import pickle  # Import pickle module for object serialization
import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from nltk.tokenize import RegexpTokenizer  # Import RegexpTokenizer for tokenizing text

import tensorflow as tf  # Import tensorflow for deep learning
from tensorflow.keras.models import Sequential, load_model  # Import Sequential model and load_model function
from tensorflow.keras.layers import Dense, Embedding, Activation  # Import layers for building neural networks
from tensorflow.keras.optimizers import RMSprop  # Import RMSprop optimizer

# import the LSTM layer
from tensorflow.keras.layers import LSTM  # Import LSTM layer for sequence modeling
from tensorflow.keras.optimizers import Adam  # Import Adam optimizer (not used here)
from tensorflow.keras.optimizers import Optimizer  # Import base Optimizer class (not used here)

text_df = pd.read_csv("fake_or_real_news.csv")  # Read the CSV file containing news data
text = list(text_df.text.values)  # Extract the 'text' column as a list
joined_text = " ".join(text)  # Join all text entries into a single string

with open("joined_text.txt", "w") as f:  # Write the joined text to a file
    f.write(joined_text)
    
partial_text = joined_text[:100000]  # Get the first 100,000 characters of the text

# Data pre processing i.e tokenization
tokenizer = RegexpTokenizer(r'\w+')  # Create a tokenizer to split text into words
tokens = tokenizer.tokenize(partial_text)  # Tokenize the partial text

# create unique tokens
unique_tokens = np.unique(tokens)  # Get unique tokens from the list

# store with index
unique_tokens_index = {}  # Create a dictionary to map tokens to indices
for i, token in enumerate(unique_tokens):  # Enumerate over unique tokens
    unique_tokens_index[token] = i  # Assign index to each token

n_words = 10  # Number of words in each input sequence
input_words = []  # List to store input sequences
next_words = []  # List to store the next word for each sequence

for i in range(len(tokens) - n_words):  # Loop over tokens to create sequences
    input_words.append(tokens[i:i + n_words])  # Add sequence of n_words
    next_words.append(tokens[i + n_words])  # Add the next word after the sequence

# Split the data into training and testing
X = np.zeros((len(input_words), n_words, len(unique_tokens)), dtype=np.bool_)  # Initialize input array
Y = np.zeros((len(next_words), len(unique_tokens)), dtype=np.bool_)  # Initialize output array

for i, words in enumerate(input_words):  # Loop over input sequences
    for j, word in enumerate(words):  # Loop over words in each sequence
        X[i, j, unique_tokens_index[word]] = 1  # Set corresponding position to 1 for each word
    Y[i, unique_tokens_index[next_words[i]]] = 1  # Set corresponding position to 1 for the next word

# Create the model
model = Sequential()  # Initialize a Sequential model

# Explain : LSTM is a type of recurrent neural network (RNN) that is capable of learning long-term dependencies. 
# It is particularly well-suited for sequence prediction problems, such as text generation.
model.add(LSTM(128, input_shape=(n_words, len(unique_tokens)), return_sequences=True))  # Add first LSTM layer
model.add(LSTM(128))  # Add second LSTM layer
model.add(Dense(len(unique_tokens)))  # Add Dense layer with output size equal to number of unique tokens
model.add(Activation('softmax'))  # Add softmax activation for output probabilities
optimizer = RMSprop(learning_rate=0.01)  # Define RMSprop optimizer with learning rate 0.01

model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])  # Compile the model

history = model.fit(X, Y, batch_size=128, epochs=10, shuffle=True).history  # Train the model and store training history
model.save("text_generator_model.h5")  # Save the trained model to a file

print(Y)  # Print the output array Y
