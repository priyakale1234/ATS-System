import streamlit as st
import tempfile

from application.resume_parser import parse_resume
from ai_engine.ranking_engine import rank_resumes
from ai_engine.ats_scoring import ats_score
from utils.pdf_generator import generate_pdf


def admin_view():
    st.title("🧑‍💼 Admin Dashboard")
    st.caption("AI-powered resume ranking, shortlisting & reports")

    jd = st.text_area(
        "📌 Job Description",
        height=200,
        placeholder="Paste job description here..."
    )

    resumes = st.file_uploader(
        "📄 Upload Multiple Resumes (PDF)",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("📊 Rank Candidates"):
        if not jd or not resumes:
            st.warning("Please upload Job Description and resumes.")
            return

        resume_texts = {}

        for file in resumes:
            resume_texts[file.name] = parse_resume(file)

        with st.spinner("Analyzing resumes using AI ATS engine..."):
            ranked_results = rank_resumes(resume_texts, jd)

        st.subheader("🏆 Candidate Ranking")

        for idx, candidate in enumerate(ranked_results, start=1):
            name = candidate["Candidate"]
            score = candidate["Score"]

            if score >= 75:
                decision = "✅ Shortlist"
            elif score >= 50:
                decision = "⚠️ Review"
            else:
                decision = "❌ Reject"

            st.markdown(
                f"""
                ### {idx}. {name}
                **ATS Score:** {score}%  
                **Decision:** {decision}
                """
            )

            with st.expander("🔍 View Detailed ATS Analysis"):
                analysis = ats_score(resume_texts[name], jd)
                st.json(analysis)

          
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                generate_pdf(analysis, tmp.name)
                pdf_bytes = open(tmp.name, "rb").read()

            st.download_button(
                label=f"📥 Download Report ({name})",
                data=pdf_bytes,
                file_name=f"{name}_ATS_Report.pdf",
                mime="application/pdf",
                key=f"download_{idx}"
            )

    st.markdown("---")
    st.caption("🔐 Admin actions are logged | AI ATS System")
