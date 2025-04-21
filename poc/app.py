import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from io import BytesIO
from pdfminer.high_level import extract_text as extract_pdf_text
from pdfminer.pdfparser import PDFSyntaxError
from docx import Document
from PIL import Image
import pytesseract
import fitz  # PyMuPDF

nltk.download("punkt")
nltk.download("stopwords")

SECTION_HEADERS = ["skills", "experience", "education", "projects", "certifications"]


def extract_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        job_description_text = ""
        for paragraph in soup.find_all("p"):
            job_description_text += paragraph.get_text() + "\n"
        return job_description_text.strip()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return None


def extract_keywords(job_description_text, predefined_skills):
    if not job_description_text:
        return []
    text = job_description_text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [w for w in tokens if not w in stop_words and w.isalnum()]
    found_skills = []
    for skill in predefined_skills:
        if skill.lower() in filtered_tokens:
            found_skills.append(skill)
    return list(set(found_skills))


def extract_text_from_pdf_or_ocr(uploaded_file):
    text = extract_pdf_text(uploaded_file)
    if text.strip():  # If actual text is found
        return text

    # Fallback: OCR for scanned PDFs
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)
    return text


def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_uploaded_cv(uploaded_file):
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        return extract_text_from_pdf_or_ocr(uploaded_file)

    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)

    else:
        st.error("Unsupported file format. Please upload a .pdf or .docx file.")
        return ""


def extract_sections(text):
    sections = {}
    lines = text.splitlines()
    current_section = None
    for line in lines:
        line_clean = line.strip().lower().rstrip(":")
        if any(h in line_clean for h in SECTION_HEADERS):
            current_section = line_clean
            sections[current_section] = []
        elif current_section and line.strip():
            sections[current_section].append(line.strip())
    return sections


def find_missing_skills(job_skills, cv_skills):
    return [skill for skill in job_skills if skill.lower() not in cv_skills]


def main():
    st.title("AI Job Agent POC (Enhanced CV Parsing)")

    keywords = st.text_input("Enter job search keywords:")
    location = st.text_input("Enter location:")
    job_url = st.text_input("Enter job description URL:")
    uploaded_cv = st.file_uploader(
        "Upload your CV (.docx or .pdf):", type=["docx", "pdf"]
    )

    predefined_skills = st.text_area(
        "Enter predefined skills (comma-separated):", "Python, Java, AWS, Communication"
    )
    skills_list = [skill.strip() for skill in predefined_skills.split(",")]

    if st.button("Analyze"):
        if job_url:
            job_description = extract_text_from_url(job_url)
            if job_description:
                extracted_job_skills = extract_keywords(job_description, skills_list)
                st.subheader("Extracted Skills from Job Description:")
                st.write(extracted_job_skills)

                cv_text = extract_text_from_uploaded_cv(uploaded_cv)
                st.subheader("Full CV Text Extracted:")
                st.text_area("CV Content Preview", cv_text, height=200)

                sections = extract_sections(cv_text)
                skills_in_cv = sections.get("skills", [])
                cv_skills_set = set([skill.lower() for skill in skills_in_cv])

                st.subheader("Skills Found in Your CV (Skills Section):")
                st.write(skills_in_cv)

                missing_skills = find_missing_skills(
                    extracted_job_skills, cv_skills_set
                )
                st.subheader("Suggested CV Updates:")
                if missing_skills:
                    st.write(
                        "The following skills mentioned in the job description are missing from your CV:"
                    )
                    for skill in missing_skills:
                        st.write(f"- {skill}")
                else:
                    st.write(
                        "No directly missing skills found based on the current analysis."
                    )
        else:
            st.warning("Please enter a job description URL.")


if __name__ == "__main__":
    main()
