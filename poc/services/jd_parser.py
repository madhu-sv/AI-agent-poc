import requests
from bs4 import BeautifulSoup

KEY_SECTIONS = [
    "responsibilities",
    "qualifications",
    "requirements",
    "skills",
    "what you'll do",
    "what we're looking for",
    "who you are",
    "about you",
]


def clean_text(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if len(line) > 3]
    return "\n".join(lines)


def extract_jd_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Combine all paragraph and list elements into text
        content_tags = soup.find_all(["p", "li", "div"])
        combined_text = "\n".join(
            [tag.get_text(separator=" ", strip=True) for tag in content_tags]
        )

        # Clean it up
        combined_text = clean_text(combined_text)

        # Try to extract only sections with relevant keywords
        lines = combined_text.split("\n")
        relevant_lines = []
        found_section = False

        for line in lines:
            lower = line.lower()
            if any(section in lower for section in KEY_SECTIONS):
                found_section = True
                relevant_lines.append("\n---\n" + line)
            elif found_section and len(line.strip()) > 0:
                relevant_lines.append(line)

        if not relevant_lines:
            # fallback: return top N lines
            return "\n".join(lines[:50])
        else:
            return "\n".join(relevant_lines[:100])

    except Exception as e:
        print(f"[JD PARSER] Failed to extract job description: {e}")
        return ""
