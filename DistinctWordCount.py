from flask import Flask, render_template, request, jsonify
from flask_api import status

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

wordnet_lemmatizer = WordNetLemmatizer()
wordnet_lemmatizer.lemmatize('is') #trigger load Wordnet into memory, slows down the start up time


@app.route('/unique_words', methods=['GET', 'POST'])
def unique_words():
    review = ''

    if request.method == 'GET':
        review = request.args.get('review')
    elif request.method == 'POST':
        review = request.json['review']

    if review == None or review == '':
        return jsonify(error='I couldn\'t find any text, please send a JSON with a "review" element that contains some text (i.e. {"review":"review text...."})')
    else:
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(review)
        stopw = set(stopwords.words('english'))
        global wordnet_lemmatizer

        distinct_words = {}
        for word in words:
            stem = wordnet_lemmatizer.lemmatize(word.lower())
            if not (word.lower() in stopw or stem in stopw):
                if not stem in distinct_words.keys():
                    distinct_words[stem] = 1
                else:
                    distinct_words[stem] += 1

        return jsonify(len=len(distinct_words.keys()), words=distinct_words)


@app.route('/relevance', methods=['GET', 'POST'])
def relevance():
    artifact = ''
    review = ''

    if request.method == 'GET':
        artifact = request.args.get('artifact')
        review = request.args.get('review')
    elif request.method == 'POST':
        artifact = request.json['artifact']
        review = request.json['review']


    if not (artifact == None or artifact == '') and (review == None or review == ''):


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3009, threaded=True)
