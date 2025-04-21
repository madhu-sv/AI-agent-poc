import streamlit as st
from services.cv_parser import extract_text_from_cv
from services.jd_parser import extract_jd_from_url
from services.skill_extractor import extract_skills
from services.comparer import compare_skills
from services.job_recommender import fetch_jobs
from services.semantic_matcher import rank_jobs_by_cv
from services.llm_tailor import generate_tailored_cv_line

st.set_page_config(page_title="AI Job Agent", layout="wide")

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "cv_skills" not in st.session_state:
    st.session_state.cv_skills = {}
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = []

st.markdown(
    """
    <style>
    .big-title { font-size: 2.8rem; font-weight: 700; margin-bottom: 0.3em; }
    .subtitle { font-size: 1.2rem; color: #555; margin-bottom: 2em; }
    .badge { background-color: #eef; color: #003366; padding: 0.3em 0.6em; border-radius: 0.5em; margin: 0.2em; display: inline-block; }
    .label-remote { background-color: #dff0d8; color: #3c763d; padding: 0.2em 0.6em; border-radius: 0.3em; font-size: 0.8rem; margin-left: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='big-title'>AI Job Agent</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Smart CV alignment and job recommendations using LLMs</div>",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["📤 Upload CV", "📊 Analyze JD", "💼 Job Recommendations"])

# --- Tab 1: CV Upload ---
with tab1:
    st.header("📄 Upload Your CV")
    cv_file = st.file_uploader("Upload your CV (.pdf or .docx)", type=["pdf", "docx"])
    if cv_file:
        st.session_state.cv_text = extract_text_from_cv(cv_file)
        st.write("### 🔍 Extracted CV Text")
        st.text_area("CV Preview", st.session_state.cv_text, height=250)

        st.write("### 🧠 Extracted Skills")
        st.session_state.cv_skills = extract_skills(
            st.session_state.cv_text, source="cv"
        )
        for category, skills in st.session_state.cv_skills.items():
            st.write(f"**{category.replace('_', ' ').title()}**")
            st.markdown(
                "".join([f"<span class='badge'>{skill}</span>" for skill in skills]),
                unsafe_allow_html=True,
            )

# --- Tab 2: Job Description Analysis ---
with tab2:
    st.header("📊 Analyze Job Description")
    job_url = st.text_input("Paste job description URL or content")

    if st.button("Analyze JD"):
        jd_text = (
            extract_jd_from_url(job_url) if job_url.startswith("http") else job_url
        )
        jd_skills = extract_skills(jd_text, source="jd")

        st.write("### 🧠 Skills in Job Description")
        st.markdown(
            "".join([f"<span class='badge'>{skill}</span>" for skill in jd_skills]),
            unsafe_allow_html=True,
        )

        if st.session_state.cv_skills:
            cv_skill_set = set(
                st.session_state.cv_skills.get("technical_skills", [])
                + st.session_state.cv_skills.get("soft_skills", [])
            )
            missing = compare_skills(
                jd_skills, {"technical_skills": list(cv_skill_set), "soft_skills": []}
            )

            st.write("### ❌ Skills Missing from CV")
            if missing:
                st.markdown(
                    "".join(
                        [f"<span class='badge'>{skill}</span>" for skill in missing]
                    ),
                    unsafe_allow_html=True,
                )
            else:
                st.success("Your CV matches all required skills!")

# --- Tab 3: Job Recommendations ---
with tab3:
    st.header("💼 Job Recommendations Based on Your CV")
    job_query = st.text_input("Job title or keywords", value="Python Developer")
    job_location = st.text_input("Location", value="London")
    job_type = st.radio(
        "Preferred Work Type:", ["Any", "Remote", "On-site", "Hybrid"], horizontal=True
    )

    if st.button("🔍 Find Matching Jobs"):
        jobs = fetch_jobs(job_query, job_location, num_results=10, job_type=job_type)

        if st.session_state.cv_text:
            jobs = rank_jobs_by_cv(st.session_state.cv_text, jobs)

        for i, job in enumerate(jobs):
            st.markdown("----")
            st.markdown(
                f"### {job['title']} <span class='label-remote'>{job.get('work_type', '')}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Company:** {job['company']}")
            st.markdown(f"**Location:** {job['location']}")
            st.markdown(f"**Type:** {job['employment_type']}")
            st.markdown(f"**Match Score:** {job.get('match_score', 0)}%")
            st.markdown(f"[Apply Here]({job['url']})", unsafe_allow_html=True)
            with st.expander("🔍 Job Description"):
                st.write(job["description"])

            if st.button(f"⭐ Save Job #{i+1}", key=f"save_{i}"):
                st.session_state.saved_jobs.append(job)
                st.success(f"Job #{i+1} saved!")

            if st.session_state.cv_text:
                if st.button(f"✏️ Suggest CV Line for Job #{i+1}", key=f"suggest_{i}"):
                    suggestion = generate_tailored_cv_line(
                        st.session_state.cv_text, job["description"]
                    )
                    st.info(f"Suggested CV Bullet:\n\n👉 {suggestion}")

    if st.session_state.saved_jobs:
        st.markdown("## ⭐ Saved Jobs")
        for saved in st.session_state.saved_jobs:
            st.markdown(
                f"**{saved['title']}** at *{saved['company']}* – {saved['location']}"
            )
