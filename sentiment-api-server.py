#!/usr/bin/env python

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect

DEBUG = False

app = Flask(__name__, static_url_path = "")

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
    data = request.data.decode("utf-8")
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
    data = request.data.decode("utf-8")
    options = { 'analyzer': naive_bayes_analyzer }
    classification, pos, neg = TextBlob(data, **options).sentiment
    return jsonify( { 'classification': classification, 'pos': pos, 'neg': neg } ), 200

vader = SentimentIntensityAnalyzer()
@app.route('/api/vader', methods = ['POST'])
def get_sentiment_vader():
    data = request.data.decode("utf-8")
    sentiments = vader.polarity_scores(data)
    sentiments['classification'] = 'neu'    
    if sentiments['compound'] > 0.1:
        sentiments['classification'] = 'pos'
    if sentiments['compound'] < -0.1:
        sentiments['classification'] = 'neg'
    return jsonify( sentiments ), 200        

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)