from flask import Flask, request, render_template, jsonify

from utils import clean_text, create_input, model, plot_sentiment

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        raw_text = request.form['input_text']
        text = clean_text(raw_text)
        token, mask = create_input(text)
        
        sentiment_result = model.predict([token, mask])
        happy = float(sentiment_result[0][0][0])
        neutral = float(sentiment_result[0][0][1])
        disappointment = float(sentiment_result[0][0][2])
        advice = float(sentiment_result[1][0][0])
        curiosity = float(sentiment_result[1][0][1])
        complaint = float(sentiment_result[1][0][2])
        
        sentiment_viz = plot_sentiment([happy, neutral, disappointment, advice, curiosity, complaint])
        
        return render_template(
            'index.html',
            raw_text=raw_text,
            sentiment_viz=sentiment_viz,
            skor_happy=happy,
            skor_neutral=neutral,
            skor_disappointment=disappointment,
            skor_advice=advice,
            skor_curiosity=curiosity,
            skor_complaint=complaint           
        )


@app.route('/api/sentiment', methods=["POST"])
def api_sentiment():
    
    raw_texts = request.get_json(force=True)['text']
    texts = [clean_text(text) for text in raw_texts]
    token_mask_set = [create_input(text) for text in texts]
    
    happy = []
    neutral = []
    disappointment = []
    advice = []
    curiosity = []
    complaint = []
    
    for token, mask in token_mask_set:
        sentiment_result = model.predict([token, mask])
        happy.append(float(sentiment_result[0][0][0]))
        neutral.append(float(sentiment_result[0][0][1]))
        disappointment.append(float(sentiment_result[0][0][2]))
        advice.append(float(sentiment_result[1][0][0]))
        curiosity.append(float(sentiment_result[1][0][1]))
        complaint.append(float(sentiment_result[1][0][2]))
    
    sentiment_result = {}
    for i, raw_text in enumerate(raw_texts):
        sentiment_result[f'result_{i}'] = {
            'id': i,
            'text': raw_text,
            'sentiment': {
                'multi-class': {
                    'happy': happy[i],
                    'neutral': neutral[i],
                    'disappointment': disappointment[i],
                },
                'multi-label': {   
                    'advice': advice[i],
                    'curiosity': curiosity[i],
                    'complaint': complaint[i],
                }
            }
        }
    
    return jsonify(sentiment_result)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)