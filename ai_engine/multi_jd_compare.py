from ai_engine.ats_scoring import ats_score

def compare_multiple_jds(resume, jd_list):
    return [ats_score(resume, jd) for jd in jd_list]
