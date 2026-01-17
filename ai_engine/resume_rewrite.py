from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rewrite_resume(resume, jd):
    prompt = f"""
Rewrite the resume to improve ATS score using job keywords.

Resume:
{resume}

Job Description:
{jd}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
