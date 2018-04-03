from __future__ import print_function

import os
import json
import string
import numpy as np
from keras.models import load_model

model_name = 'model'
max_features = 5000
maxlen = 400

# load model
model = load_model(model_name + '.h5')

# load vocab
with open('vocab.json') as json_data:
    vocab = json.load(json_data)
    w_i = vocab['word_to_index']
    i_w = vocab['index_to_word']

def get_sentence(embedings, i_w=i_w):
    return ' '.join( '' if id<=1 else i_w[id] for id in embedings ).strip()

def sentence_to_embedings(txt, w_i=w_i, maxlen=maxlen):
    exclude_char = set(string.punctuation)
    txt = ''.join(ch for ch in txt if ch not in exclude_char)
    words = txt.replace('  ',' ').split(' ')
    word_idx = [ w_i[w] if w in w_i else 2 for w in words ][:maxlen-1]
    pad_count = maxlen - 1 - len(word_idx)
    padded = [ 0 for i in range(pad_count)]
    return padded + [1] + word_idx

def predict_one(text, model=model):
    embedings = np.array([sentence_to_embedings(text)])
    prediction = model.predict(embedings)[0][0]
    prediction = prediction * 2 - 1
    return json.dumps( {'classification': 'pos' if prediction > 0 else 'neg' if prediction < 0 else 'neu', 'sentiment': round(prediction, 2)} )
  
def predict(texts, model=model):
    embedings = np.array([sentence_to_embedings(text) for text in texts])
    predictions = model.predict(embedings)
    predictions = predictions * 2 - 1
    return json.dumps([ {'classification': 'pos' if pred[0] > 0 else 'neg' if prediction < 0 else 'neu', 'sentiment': round(pred[0], 2)} for pred in predictions])

print(predict_one('hello'))