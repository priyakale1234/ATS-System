from application.resume_parser import parse_resume
from ai_engine.ats_scoring import ats_score

def run_full_ats(resume_file, jd):
    resume_text = parse_resume(resume_file)
    result = ats_score(resume_text, jd)
    result["resume_text"] = resume_text
    return result
