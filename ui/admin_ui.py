import streamlit as st
import os

from application.resume_parser import parse_resume
from ai_engine.ranking_engine import rank_resumes
from ai_engine.ats_scoring import ats_score
from utils.pdf_generator import generate_pdf   # ✅ FIXED IMPORT


def admin_view():
    st.title("🧑‍💼 Admin Dashboard")
    st.caption("AI-powered resume ranking, shortlisting & reports")

    # ==============================
    # JOB DESCRIPTION INPUT
    # ==============================
    jd = st.text_area(
        "📌 Job Description",
        height=200,
        placeholder="Paste job description here..."
    )

    # ==============================
    # MULTIPLE RESUME UPLOAD
    # ==============================
    resumes = st.file_uploader(
        "📄 Upload Multiple Resumes (PDF)",
        type="pdf",
        accept_multiple_files=True
    )

    # ==============================
    # RANK CANDIDATES
    # ==============================
    if st.button("📊 Rank Candidates"):
        if not jd or not resumes:
            st.warning("Please upload Job Description and resumes.")
            return

        resume_texts = {}

        # Parse resumes
        for file in resumes:
            resume_texts[file.name] = parse_resume(file)

        # Ranking
        with st.spinner("Analyzing resumes using AI ATS engine..."):
            ranked_results = rank_resumes(resume_texts, jd)

        st.subheader("🏆 Candidate Ranking")

        # ==============================
        # DISPLAY RESULTS
        # ==============================
        for idx, candidate in enumerate(ranked_results, start=1):
            name = candidate["Candidate"]
            score = candidate["Score"]

            # Decision Logic
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

           
         
            report_path = f"data/reports/{name}_ATS_Report.pdf"

            if st.button(
                f"📥 Download Report ({name})",
                key=f"download_{idx}"   
            ):
                generate_pdf(analysis, report_path)
                st.success(f"Report saved to {report_path}")

  
    st.markdown("---")
    st.caption("🔐 Admin actions are logged | AI ATS System")
