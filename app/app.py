from flask import Flask, request, render_template
import os
import random
import socket
import sys
import json
import pickle
import tflearn
import tensorflow as tf
import nltk
from flask_cors import CORS

from nltk.stem.lancaster import LancasterStemmer
import numpy as np
app = Flask(__name__)

print('init')
nltk.download('punkt')
tf.reset_default_graph()
data = pickle.load( open( "training_data", "rb" ) ) 
data = pickle.load( open( "training_data", "rb" ) )
train_x = data['train_x']
train_y = data['train_y']
words = data['words']
classes = data['classes']
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')

app.config.from_pyfile('config_file.cfg')
# reset underlying graph data# reset 
tf.reset_default_graph()

if ("VOTE1VALUE" in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    stemmer = LancasterStemmer()
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    print('from cleaning:')
    print(sentence_words)
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))
def classify(sentence):
    # generate probabilities from the model
    ERROR_THRESHOLD = 0.25
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return str(return_list)
result = str(classify("Hello, how are you?"))

@app.route('/', methods=['GET', 'POST'])
def hello():
    # [model, data, intents] = loadModule.loadmymodule()
    # def getAnswer(sentence):
    #     sentence = rp.classify(model, data, request.form['sentence'])
    #     return sentence

    if request.method == 'GET':

        return render_template("index.html", value1='sentence', button1=button1, title=title)

    elif request.method == 'POST':
        print(3)
        if request.form['vote'] == 'send':
            # if len(sentence) > 0:
            return render_template("index.html", value1=classify(request.form['sentence']), button1=button1, title=title)
            # else:
            #     return render_template("index.html", value1="Sorry, I don't understand", button1=button1, title=title)
        else:
            # if len(sentence) > 0:
            #     return render_template("index.html", value1="Sorry, I don't understand", button1=button1, title=title)

            
            return render_template("index.html", value1=classify(request.form['sentence']), button1=button1, title=title)
if __name__ == "__main__":
    app.run(debug=1)
