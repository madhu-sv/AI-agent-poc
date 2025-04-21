import os
import requests

JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"
JSEARCH_API_KEY = os.getenv("RAPIDAPI_KEY")  # Set this in your .env


def fetch_jobs(query, location="United Kingdom", num_results=10):
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    params = {"query": query, "location": location, "page": 1, "num_pages": 1}

    try:
        response = requests.get(JSEARCH_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        jobs = data.get("data", [])[:num_results]

        # Simplify the result structure
        simplified = []
        for job in jobs:
            simplified.append(
                {
                    "title": job.get("job_title"),
                    "company": job.get("employer_name"),
                    "description": job.get("job_description"),
                    "location": job.get("job_city"),
                    "employment_type": job.get("job_employment_type"),
                    "url": job.get("job_apply_link"),
                }
            )
        return simplified

    except requests.exceptions.RequestException as e:
        print(f"[JSEARCH ERROR] {e}")
        return []
