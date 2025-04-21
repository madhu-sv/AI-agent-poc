# 🧠 AI Job Agent – Proof of Concept

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 A prototype tool to help job seekers intelligently compare their CVs against job postings and discover actionable insights to enhance their resume.

---

## 📸 Demo Screenshot

> _Coming Soon!_  
> Add a screenshot like:

```markdown
![Demo Screenshot](assets/demo.png)
```
## 🔗 Table of Contents
[Overview](#overview)

[Features](#features)

[Getting Started](#gettingstarted)

[Running the App](#runningtheapp)

[Project Structure](#structure)

[Limitations](#limitations)

[Planned Enhancements](#enhancements)

[License](#license)

# 🧭 Overview <a name="overview"></a>
The AI Job Agent is a Python-based tool that helps job seekers tailor their CVs for specific roles by:

Parsing job description content from a provided URL

Extracting skills using NLP

Parsing CVs in .pdf or .docx format (with OCR fallback for scanned PDFs)

Suggesting which skills to add based on a predefined or custom skill list

# ✨ Features <a name="features"></a>
✅ Upload .pdf or .docx CVs

✅ Extract job description content from a URL

✅ Auto-detect CV sections (skills, experience, education)

✅ Basic keyword-based skill matching

✅ OCR support for scanned/image-based PDFs

✅ Streamlit-powered UI – no setup beyond Python required


# ⚙️ Getting Started <a name="gettingstarted"></a>
🐍 Install Python Packages
```bash
pip install -r requirements.txt
```
🍎 macOS System Dependencies (via Homebrew)
```bash
brew install tesseract
brew install poppler
brew install ghostscript
```
🐧 Ubuntu/Linux Equivalent
```bash
sudo apt update
sudo apt install tesseract-ocr poppler-utils ghostscript
```
⚠️ tesseract is required for OCR (image-based PDFs)

▶️ Running the App <a name="runningtheapp"></a>
Create a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
Start the app:

```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

# 🗂 Project Structure <a name="structure"></a>
```bash
ai-job-agent-poc/
├── app.py                # Streamlit app
├── requirements.txt
├── README.md
├── sample_cv.pdf         # (Optional) Example CV for testing
└── assets/               # (Optional) Screenshots or visual assets
```
# ⚠️ Limitations <a name="limitations"></a>
LinkedIn data must be input manually (no API integration)

Skill extraction uses basic keyword matching (NLP not context-aware)

Does not currently assess experience level or frequency of skills

Suggestions are not generated in full sentences (just skill gaps)

# 🧪 Planned Enhancements <a name="enhancements"></a>
Semantic skill extraction using spaCy or Transformers

Section-aware matching (skills vs experience vs certifications)

Smart rewriting suggestions using LLMs

Export suggestions into an updated CV draft

Online deployment (Streamlit Cloud or Hugging Face Spaces)

# 📜 License <a name="license"></a>
This project is licensed under the MIT License.

# 🙋‍♀️ Contributions
Ideas, suggestions, and pull requests are welcome!
Let’s make job hunting smarter together.
