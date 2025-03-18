# score_messages.py
# Keyword scoring logic for LinkedIn message prioritization

import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd

for resource in ['punkt', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        print(f"Downloading '{resource}'...")
        nltk.download(resource, force=True)

stemmer = PorterStemmer()

scoring_rules = {
    # Positive Keywords (Important)
    "resume": 10,
    "project": 10,
    "portfolio": 10,
    "hire": 15,
    "collaboration": 10,
    "interview": 15,
    "work": 5,
    "team": 5,
    # Negative Keywords (Spam/Low Value)
    "sales": -10,
    "buy": -10,
    "offer": -10,
    "discount": -10,
    "free": -10,
    "hi": -5,
    "how are you": -5,
    "hello": -2,
}

stemmed_rules = {stemmer.stem(keyword): value for keyword, value in scoring_rules.items()}

def score_message(message):
    score = 0
    message_lower = message.lower()

    words = word_tokenize(message_lower)
    stemmed_words = [stemmer.stem(word) for word in words]
    
    for stemmed_keyword, value in stemmed_rules.items():
       if " " not in stemmed_keyword and stemmed_keyword in stemmed_words:
            score += value
    
    # Bonuses
    url_match = re.search(r"http[s]?://|www\.|\.com", message_lower)
    if url_match:
        score += 5
    word_count = len(words)
    if word_count >= 20:
        score += 3
    num_match = re.search(r"\d", message_lower)
    if num_match:
        score += 2
    
    # Penalties
    if word_count < 5:
        score -= 5
    if message.strip() and message == message.upper() and any(c.isalpha() for c in message):
        score -= 3

    return score

def read_messages(file_path):
    messages = []
    try:
        df = pd.read_csv(file_path)
        if 'message' in df.columns:
            messages = df['message'].dropna().tolist()
        else:
            raise ValueError("CSV file must have a 'message' column")
    except (pd.errors.EmptyDataError, ValueError, FileNotFoundError):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                messages = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return []
    print(f"Read {len(messages)} messages from {file_path}")
    return messages

def categorize_message(score):
    """Assign a category based on score."""
    if score >= 15:
        return "Priority"
    elif score >= 0:
        return "Maybe"
    else:
        return "Spam"
    
def update_scoring_rules(keyword, score):
    global scoring_rules, stemmed_rules
    scoring_rules[keyword] = int(score)  # Ensure score is an integer
    stemmed_rules = {stemmer.stem(k): v for k, v in scoring_rules.items()}

def process_and_save_messages(file_path, output_file="scored_messages.csv"):
    messages = read_messages(file_path)
    results = [{"message": msg, "score": score_message(msg)} for msg in messages]
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    for result in sorted_results:
        result["category"] = categorize_message(result["score"])
    df = pd.DataFrame(sorted_results, columns=["message", "score", "category"])
    df.to_csv(output_file, index=False)
    return sorted_results
