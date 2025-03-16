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
    print(f"\nProcessing: {message}")

    words = word_tokenize(message_lower)
    stemmed_words = [stemmer.stem(word) for word in words]
    print(f"Stemmed words: {stemmed_words}")
    
    for stemmed_keyword, value in stemmed_rules.items():
        if stemmed_keyword in stemmed_words:
            print(f"Matched '{stemmed_keyword}' = {value}")
            score += value
    
    # Bonuses
    url_match = re.search(r"http[s]?://|www\.|\.com", message_lower)
    if url_match:
        print(f"Matched URL at {url_match.span()} = +5")
        score += 5
    word_count = len(words)
    print(f"Word count: {word_count}")
    if word_count >= 20:
        print("Long message (>20 words): +3")
        score += 3
    num_match = re.search(r"\d", message_lower)
    if num_match:
        print(f"Matched number at {num_match.span()} = +2")
        score += 2
    
    # Penalties
    if word_count < 5:
        print("Short message (<5 words): -5")
        score -= 5
    if message.strip() and message == message.upper() and any(c.isalpha() for c in message):
        print("All caps message: -3")
        score -= 3

    return score

def read_messages(file_path):
    """Read messages from a CSV or TXT file into a list."""
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

def main():
    file_path = "test_messages.txt"  
    messages = read_messages(file_path)
    for msg in messages:
        print(f"Message: {msg}")

if __name__ == "__main__":
    main()

