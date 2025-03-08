# score_messages.py
# Keyword scoring logic for LinkedIn message prioritization

import re

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
    "hello": -5
}

def score_message(message):
    score = 0
    message_lower = message.lower()  
    
    for keyword, value in scoring_rules.items():
        if re.search(rf"\b{keyword}\b", message_lower): 
            score += value
    
    return score

def main():
    test_messages = [
        "Here’s my resume and project link",
        "Buy my product now!",
        "Hi, how are you?"
    ]
    for msg in test_messages:
        score = score_message(msg)
        print(f"Message: {msg} | Score: {score}")

if __name__ == "__main__":
    main()