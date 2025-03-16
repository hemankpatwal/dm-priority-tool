from flask import Flask, render_template, request, jsonify
from score_messages import score_message, read_messages, categorize_message
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    try:
        df = pd.read_csv('scored_messages.csv')
        messages = df.to_dict('records') 
    except FileNotFoundError:
        messages = [{"message": "No data yet—run score_messages.py first!", "score": 0, "category": "N/A"}]
    
    return render_template('index.html', messages=messages)

@app.route('/score', methods=['POST'])
def score():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    score = score_message(message)
    category = categorize_message(score)
    return jsonify({'message': message, 'score': score, 'category': category})

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)