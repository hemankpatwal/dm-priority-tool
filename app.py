from flask import Flask, render_template
from score_messages import score_message, read_messages
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

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)