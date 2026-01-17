import streamlit as st
from ui.candidate_ui import candidate_view
from ui.admin_ui import admin_view

st.set_page_config("AI ATS Platform", "📄", layout="wide")

role = st.sidebar.radio("Select Role", ["Candidate", "Admin"])

if role == "Candidate":
    candidate_view()
else:
    admin_view()
