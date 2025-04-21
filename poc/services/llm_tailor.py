from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_tailored_cv_line(cv_text, job_description):
    prompt = (
        "Based on the following CV and job description, suggest one bullet point the user can add to tailor their CV for this job. "
        "The response should be a single bullet point.\n\n"
        f"CV:\n{cv_text}\n\nJob Description:\n{job_description}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating suggestion: {e}"
