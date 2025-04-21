import streamlit as st
from services.cv_parser import extract_text_from_cv
from services.jd_parser import extract_jd_from_url
from services.skill_extractor import extract_skills
from services.comparer import compare_skills

st.title("AI Job Agent - POC")

st.write("This is a basic Proof-of-Concept to compare your CV to a job description.")

job_url = st.text_input("Enter job description URL:")
cv_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

if st.button("Run Analysis"):
    if job_url and cv_file:
        jd_text = extract_jd_from_url(job_url)
        jd_skills = extract_skills(jd_text, source="jd")

        st.subheader("Skills from Job Description")
        st.write(jd_skills)

        cv_text = extract_text_from_cv(cv_file)
        cv_skills = extract_skills(cv_text, source="cv")

        st.subheader("Skills from Your CV")
        st.write(cv_skills)

        # Flatten CV skill dict
        cv_skill_set = set(
            cv_skills.get("technical_skills", []) + cv_skills.get("soft_skills", [])
        )
        missing_skills = compare_skills(
            jd_skills, {"technical_skills": list(cv_skill_set), "soft_skills": []}
        )

        st.subheader("Suggested Skills to Add")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- {skill}")
        else:
            st.success("Your CV covers all required job skills.")
    else:
        st.warning("Please upload your CV and enter a job URL.")
