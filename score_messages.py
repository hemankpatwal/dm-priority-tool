# score_messages.py
# Keyword scoring logic for LinkedIn message prioritization

import re

scoring_rules = {
    # Positive Keywords (Important)
    "resume": 10,
    "project": 10,
    "portfolio": 10,
    "hire": 15,
    "hiring": 15,
    "collaboration": 10,
    "collaborating": 10,
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
    "hello": -5
}

def score_message(message):
    score = 0
    message_lower = message.lower()
    print(f"\nProcessing: {message}")
    
    for keyword, value in sorted(scoring_rules.items(), key=lambda x: -len(x[0])):
        match = re.search(rf"\b{keyword}\b", message_lower)
        if match:
            print(f"Matched '{keyword}' at {match.span()} with '{match.group()}' = {value}")
            score += value
    
    # Bonuses
    url_match = re.search(r"http[s]?://|www\.|\.com", message_lower)
    if url_match:
        print(f"Matched URL at {url_match.span()} = +5")
        score += 5
    words = message_lower.split()
    print(f"Word count: {len(words)}")
    if len(words) > 20:
        print("Long message (>20 words): +3")
        score += 3
    num_match = re.search(r"\d", message_lower)
    if num_match:
        print(f"Matched number at {num_match.span()} = +2")
        score += 2
    
    return score

def main():
    test_messages = [
        "Hiring you for a project with 2 years experience",
        "Collaborating on a project sounds great"
    ]
    for msg in test_messages:
        score = score_message(msg)
        print(f"Message: {msg} | Score: {score}")

if __name__ == "__main__":
    main()