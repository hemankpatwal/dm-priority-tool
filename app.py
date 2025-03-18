from flask import Flask, render_template, request, jsonify
from score_messages import score_message, read_messages, categorize_message, update_scoring_rules, process_and_save_messages, scoring_rules
import pandas as pd

app = Flask(__name__)
INPUT_FILE = "test_messages.txt"

@app.route('/')
def home():
    try:
        df = pd.read_csv('scored_messages.csv')
        messages = df.to_dict('records') 
    except FileNotFoundError:
        messages = process_and_save_messages(INPUT_FILE)
    
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

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    data = request.get_json()
    keyword = data.get('keyword', '').strip()
    score = data.get('score', '')
    
    if not keyword or not score:
        return jsonify({'error': 'Keyword and score are required'}), 400
    try:
        score = int(score) 
    except ValueError:
        return jsonify({'error': 'Score must be an integer'}), 400
    
    update_scoring_rules(keyword, score)
    try:
        updated_messages = process_and_save_messages(INPUT_FILE)
    except FileNotFoundError:
        return jsonify({'error': f"Input file '{INPUT_FILE}' not found"}), 500
    
    return jsonify({'success': 'Keyword added', 'messages': updated_messages})

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    return jsonify({'keywords': scoring_rules})

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)