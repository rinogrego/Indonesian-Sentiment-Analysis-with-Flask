from flask import Flask, request, render_template, jsonify
import json

import numpy as np
from utils import clean_text, create_input, model

# import matplotlib.pyplot as plt
import base64
import io


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/api/sentiment', methods=["POST"])
def api_sentiment():
    
    raw_text = request.get_json(force=True)['text']
    text = clean_text(raw_text)
    token, mask = create_input(text)
    
    sentiment_result = model.predict([token, mask])
    sentiment_result = {
        'text': raw_text,
        'sentiment': {
            'multi-class': {
                'happy': float(sentiment_result[0][0][0]),
                'neutral': float(sentiment_result[0][0][1]),
                'disappointment': float(sentiment_result[0][0][2]),
            },
            'multi-label': {   
                'advice': float(sentiment_result[1][0][0]),
                'curiosity': float(sentiment_result[1][0][1]),
                'complaint': float(sentiment_result[1][0][2]),
            }
        }
    }
    
    return jsonify(sentiment_result)


if __name__ == '__main__':
    app.run(debug=True)