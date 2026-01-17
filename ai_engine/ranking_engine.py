from ai_engine.ats_scoring import ats_score

def rank_resumes(resumes, jd):
    ranked = []
    for name, text in resumes.items():
        r = ats_score(text, jd)
        ranked.append({"Candidate": name, "Score": r["ats_score"]})
    return sorted(ranked, key=lambda x: x["Score"], reverse=True)
