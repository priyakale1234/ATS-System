from groq import Groq
import os
from dotenv import load_dotenv
from utils.helpers import safe_json_loads, normalize_score, verdict_from_score

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ats_score(resume, jd):
    prompt = f"""
You are an ATS engine.

STRICT RULES:
- Output ONLY valid JSON
- No explanations
- No markdown
- No text outside JSON

JSON FORMAT:
{{
  "ats_score": 0-100,
  "missing_skills": [],
  "strengths": [],
  "improvements": []
}}

Resume:
{resume}

Job Description:
{jd}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content

  
    data = safe_json_loads(raw_output)

   
    if not data:
        data = {
            "ats_score": 0,
            "missing_skills": [],
            "strengths": [],
            "improvements": ["Unable to parse AI response"]
        }

  
    score = normalize_score(data.get("ats_score", 0))
    data["ats_score"] = score
    data["verdict"] = verdict_from_score(score)

    return data
