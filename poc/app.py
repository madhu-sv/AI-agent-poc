import streamlit as st
from services.cv_parser import extract_text_from_cv
from services.jd_parser import extract_jd_from_url
from services.skill_extractor import extract_skills
from services.comparer import compare_skills

# --- UI Styling ---
st.set_page_config(page_title="AI Job Agent", layout="centered")

st.markdown(
    """
    <style>
        .big-title {
            font-size: 3em;
            font-weight: 600;
            margin-bottom: 0.3em;
        }
        .subtitle {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 2em;
        }
        .card {
            background-color: #fff;
            padding: 2em;
            border-radius: 1rem;
            box-shadow: 0 5px 25px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }
        .stTextInput > label, .stFileUploader > label {
            font-weight: 500;
        }
        .stButton button {
            background-color: #4461F2;
            color: white;
            padding: 0.6em 1.4em;
            border-radius: 0.6em;
            font-weight: 500;
            margin-top: 1em;
        }
        #MainMenu, header, footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# --- UI Header ---
st.markdown("<div class='big-title'>AI Job Agent</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Smarter job matching with LLM-powered CV & JD analysis</div>",
    unsafe_allow_html=True,
)

# --- User Input Card ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    job_url = st.text_input("🔗 Job Description URL")
    cv_file = st.file_uploader(
        "📄 Upload your CV (.pdf or .docx)", type=["pdf", "docx"]
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --- Analysis Trigger ---
if st.button("✨ Analyze"):
    if not job_url or not cv_file:
        st.warning("Please provide both a job URL and a CV file.")
    else:
        jd_text = extract_jd_from_url(job_url)
        cv_text = extract_text_from_cv(cv_file)

        jd_skills = extract_skills(jd_text, source="jd")
        cv_skills = extract_skills(cv_text, source="cv")

        # --- Results Output ---
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## 📄 Job Description Preview")
        st.write(jd_text[:1000] + "..." if len(jd_text) > 1000 else jd_text)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## 💼 CV Preview")
        st.write(cv_text[:1000] + "..." if len(cv_text) > 1000 else cv_text)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## 🧠 Extracted Skills from JD")
        st.json(jd_skills)
        st.markdown("## 🧠 Extracted Skills from CV")
        st.json(cv_skills)
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Skill Comparison ---
        missing_skills = compare_skills(jd_skills, cv_skills)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("## 📌 Suggested Skills to Add")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"🔹 {skill}")
        else:
            st.success("🎉 Your CV covers all major skills from the JD!")
        st.markdown("</div>", unsafe_allow_html=True)
