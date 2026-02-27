import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/resumes/generate"

st.set_page_config(page_title="AI Resume & Portfolio Builder", layout="wide")

st.title("AI Resume & Portfolio Builder")
st.write("Fill in your details and job info, then generate a tailored resume.")

with st.form("resume_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        email = st.text_input("Email")
        skills = st.text_area("Skills (comma-separated)")
        education = st.text_area("Education")

    with col2:
        job_title = st.text_input("Target Job Title")
        job_description = st.text_area("Job Description (paste JD here)")

    submitted = st.form_submit_button("Generate Resume")

if submitted:
    if not name or not email or not job_title:
        st.error("Name, Email, and Job Title are required.")
    else:
        with st.spinner("Generating resume..."):
            payload = {
                "name": name,
                "email": email,
                "skills": skills,
                "education": education,
                "job_title": job_title,
                "job_description": job_description,
            }
            try:
                res = requests.post(API_URL, json=payload, timeout=60)
                res.raise_for_status()
                data = res.json()
                resume_text = data.get("resume_text") or str(data)
                st.success("Resume generated!")
                st.subheader("Generated Resume")
                st.text_area("Resume", resume_text, height=400)
            except Exception as e:
                st.error(f"Failed to generate resume: {e}")
