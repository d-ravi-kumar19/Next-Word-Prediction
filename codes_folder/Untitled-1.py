# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.datasets import reuters
from tensorflow.keras.layers import Embedding,LSTM,Bidirectional,Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# %%

data = pd.read_csv('medium_data.csv')
data['title']
print(data.shape)


# %%
data ['title'] = data['title'].apply(lambda x: x.replace(u'\xa0',u' ').replace('\u200a',' '))

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['title'])
total_words = len(tokenizer.word_index) + 1

print("Total number of words: ", total_words)

# %%
input_sequences = []

for line in data['title']:
  # print(line)
  token_list = tokenizer.texts_to_sequences([line])[0]
  # print(token_list)
  for i in range(1,len(token_list)):
    n_gram_sequence = token_list[:i+1]
    input_sequences.append(n_gram_sequence)

print("total input sequences:",len(input_sequences))

# %%
# input_sequences = np.array(input_sequences)
max_sequence_length = max(len(seq) for seq in input_sequences)
print("Max Sequence Length:", max_sequence_length)
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre'))
X,y = input_sequences[:,:-1],input_sequences[:,-1]
y = tf.keras.utils.to_categorical(y, num_classes = total_words)


# %%
model = Sequential()
model.add(Embedding(total_words,100,input_length= max_sequence_length-1 ))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_words,activation = 'softmax'))

model.compile(optimizer ='adam', loss ='categorical_crossentropy',metrics= ['accuracy'])
model.summary()

# %%
history = model.fit(X,y,epochs =50,verbose=1)
print(model)

# %%
history

# %%
import h5py
model_filename = 'model.h5'
model.save(model_filename)

# %%
def plot_graphs(history,metric):
  plt.plot(history.history[metric])
  plt.xlabel('Epochs')
  plt.ylabel(metric)
  plt.show()

plot_graphs(history,'accuracy')

# %%
plot_graphs(history,'loss')

# %%
def predict_next_word(seed_text, model, tokenizer, max_sequence_length):
    for _ in range(3):  # Predict the next 3 words
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length-1, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)[0]
        predicted_id = np.argmax(predicted_probs)
        predicted_word = tokenizer.index_word[predicted_id]
        seed_text += " " + predicted_word
    return seed_text

seed_text = "hypothesis"
predicted_text = predict_next_word(seed_text, model, tokenizer, max_sequence_length)
print("Seed text:", seed_text)
print("Predicted next words:", predicted_text)

