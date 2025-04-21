import os
import requests

JSEARCH_API_URL = "https://jsearch.p.rapidapi.com/search"
JSEARCH_API_KEY = os.getenv("RAPIDAPI_KEY")


def fetch_jobs(query, location="United Kingdom", num_results=10, job_type="Any"):
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    params = {"query": query, "location": location, "page": 1, "num_pages": 1}

    try:
        response = requests.get(JSEARCH_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        jobs = data.get("data", [])

        def matches_type(job):
            desc = (job.get("job_description") or "").lower()
            title = (job.get("job_title") or "").lower()
            is_remote = (
                "remote" in desc or "remote" in title or job.get("job_is_remote")
            )

            if job_type == "Remote":
                return is_remote
            elif job_type == "On-site":
                return not is_remote
            elif job_type == "Hybrid":
                return "hybrid" in desc or "hybrid" in title
            return True

        filtered_jobs = [job for job in jobs if matches_type(job)]

        # Add 'work_type' label
        for job in filtered_jobs:
            desc = (job.get("job_description") or "").lower()
            title = (job.get("job_title") or "").lower()
            if "remote" in desc or "remote" in title:
                job["work_type"] = "Remote"
            elif "hybrid" in desc or "hybrid" in title:
                job["work_type"] = "Hybrid"
            else:
                job["work_type"] = "On-site"

        return [
            {
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "description": job.get("job_description"),
                "location": job.get("job_city"),
                "employment_type": job.get("job_employment_type"),
                "url": job.get("job_apply_link"),
                "job_is_remote": job.get("job_is_remote"),
                "work_type": job.get("work_type"),
            }
            for job in filtered_jobs[:num_results]
        ]

    except requests.exceptions.RequestException as e:
        print(f"[JSEARCH ERROR] {e}")
        return []
