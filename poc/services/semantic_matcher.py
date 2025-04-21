import os
import numpy as np
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(model=model, input=[text])
    return np.array(response.data[0].embedding)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def rank_jobs_by_cv(cv_text, jobs):
    try:
        cv_embed = get_embedding(cv_text)

        ranked = []
        for job in jobs:
            job_text = job["description"] or job["title"]
            job_embed = get_embedding(job_text)
            score = cosine_similarity(cv_embed, job_embed)
            job["match_score"] = round(score * 100, 2)
            ranked.append(job)

        return sorted(ranked, key=lambda j: j["match_score"], reverse=True)

    except Exception as e:
        print(f"[EMBEDDING ERROR] {e}")
        return jobs
