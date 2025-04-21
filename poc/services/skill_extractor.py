import json
import hashlib
from openai import OpenAI
# This module is responsible for extracting skills from job descriptions and CVs using OpenAI's API.
# It caches the results to avoid redundant API calls and improve performance.
# It also provides utility functions for managing the cache and summarizing its contents.
# Ensure you have the OpenAI API key set in your environment variables
# as OPENAI_API_KEY.
# This code uses the OpenAI Python client library to interact with the API.

import os


openai_api_key = os.getenv("OPENAI_API_KEY")


# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# File-based cache for skills extracted from job descriptions and CVs
CACHE_FILE = "skill_cache.json"

# Load existing cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        skill_cache = json.load(f)
else:
    skill_cache = {}

def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()

def extract_skills(text, source="jd"):
    import logging
    logging.basicConfig(level=logging.INFO)

    key = f"{source}_{hash_text(text)}"
    if key in skill_cache:
        logging.info(f"[CACHE HIT] Using cached result for {source.upper()} (hash: {key})")
        return skill_cache[key]

    prompt = (
        f"Extract a JSON list of relevant skills from this job description:\n\n{text}"
        if source == "jd"
        else f"Extract technical_skills and soft_skills from this CV. Return in JSON:\n\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )

        content = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {"raw_output": content}

        logging.info(f"[CACHE MISS] Caching result for {source.upper()} (hash: {key})")
        skill_cache[key] = parsed
        with open(CACHE_FILE, "w") as f:
            json.dump(skill_cache, f, indent=2)

        return parsed

    except Exception as e:
        return {"error": str(e)}

# Utility function for offline cache management

def clear_skill_cache():
    global skill_cache
    skill_cache = {}
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


def get_cache_summary():
    return {
        "total_entries": len(skill_cache),
        "job_descriptions": len([k for k in skill_cache if k.startswith("jd_")]),
        "cvs": len([k for k in skill_cache if k.startswith("cv_")])
    }
