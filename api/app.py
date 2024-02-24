from flask import Flask,render_template,request,jsonify
from keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences
import joblib
# import json
import numpy as np

app = Flask(__name__)
model = load_model('models/gru_model.h5')
tokenizer = joblib.load('models/tokenizer.joblib')

def generate_suggestions(search_text):
    suggestions = ""
    next_words = 3
    max_sequence_len = 40
    try:
        for _ in range(next_words):
            token_list = tokenizer.texts_to_sequences([search_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
            predicted_probs = model.predict(token_list, verbose=0)[0]
            predicted_index = np.argmax(predicted_probs)


            # print(predicted_index)
            output_word = ""
            for word, index in tokenizer.word_index.items():
                if index == predicted_index:
                    output_word = word
                    # print(output_word)
                    break
            suggestions = search_text + " " + output_word
    except Exception:
        pass
    # print("suggestions:  ",suggestions)
    return suggestions

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    search_text = request.form['search_text'].lower()
    # print("Search text:",search_text)
    matching_words = generate_suggestions(search_text)
    return jsonify(matching_words)

if __name__ == '__main__':
    app.run(debug= True)