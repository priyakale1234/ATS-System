import json
import re

def safe_json_loads(text: str) -> dict:
    """
    Safely extracts JSON from LLM output.
    """
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return {}
        return {}

def normalize_score(score):
    try:
        score = int(score)
        return max(0, min(score, 100))
    except:
        return 0

def verdict_from_score(score):
    if score >= 75:
        return "Strong"
    elif score >= 50:
        return "Moderate"
    return "Weak"
