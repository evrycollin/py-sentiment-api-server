#!/usr/bin/env python
import string
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect
import demo

DEBUG = False
exclude_char = set(string.punctuation)

app = Flask(__name__, static_url_path = "")

# to lower case + remove punctuation + remove long spaces + trim
def clean_data(str):
    txt = str.lower()
    txt = ''.join(ch for ch in txt if ch not in exclude_char)
    return txt.replace('  ',' ').strip()

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/api/textblob', methods = ['POST'])
def get_sentiment_textblob():
    data = clean_data(request.data.decode("utf-8"))
    polarity, subjectivity = TextBlob(data).sentiment
    classification = 'neu'
    if subjectivity > 0:
        if polarity > 0:
            classification = 'pos'
        if polarity < 0:
            classification = 'neg'
    return jsonify( { 'classification': classification,'polarity': polarity, 'subjectivity': subjectivity } ), 200        

naive_bayes_analyzer = NaiveBayesAnalyzer()
@app.route('/api/textblob/naive-bayes', methods = ['POST'])
def get_sentiment_textblob_nb():
    data = clean_data(request.data.decode("utf-8"))
    options = { 'analyzer': naive_bayes_analyzer }
    classification, pos, neg = TextBlob(data, **options).sentiment
    return jsonify( { 'classification': classification, 'pos': pos, 'neg': neg } ), 200

vader = SentimentIntensityAnalyzer()
@app.route('/api/vader', methods = ['POST'])
def get_sentiment_vader():
    data = clean_data(request.data.decode("utf-8"))
    sentiments = vader.polarity_scores(data)
    sentiments['classification'] = 'neu'    
    if sentiments['compound'] > 0.1:
        sentiments['classification'] = 'pos'
    if sentiments['compound'] < -0.1:
        sentiments['classification'] = 'neg'
    return jsonify( sentiments ), 200        

@app.route('/api/demo', methods = ['POST'])
def get_sentiment_demo_ai():
    return demo.predict_one(request.data.decode("utf-8")), 200 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)