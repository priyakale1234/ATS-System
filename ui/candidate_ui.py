import streamlit as st
from application.ats_controller import run_full_ats
from ai_engine.resume_rewrite import rewrite_resume

def candidate_view():
    st.title("👤 Candidate Portal")
    jd = st.text_area("📌 Job Description", height=200)
    resume = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")

    if st.button("🔍 Analyze Resume"):
        if resume and jd:
            result = run_full_ats(resume, jd)
            st.metric("ATS Score", f"{result['ats_score']}%")
            st.json(result)
        else:
            st.warning("Upload resume and JD")

    if st.button("✍️ Rewrite Resume"):
        if resume and jd:
            rewritten = rewrite_resume(run_full_ats(resume, jd)["resume_text"], jd)
            st.subheader("Rewritten Resume")
            st.write(rewritten)
