import re

def extract_keywords(text):
    words = re.findall(r"\b[A-Za-z]{3,}\b", text.lower())
    return list(set(words))
