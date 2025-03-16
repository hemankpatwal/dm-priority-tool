from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World! This is your LinkedIn message prioritizer."

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)