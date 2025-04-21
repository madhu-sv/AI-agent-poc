def compare_skills(jd_skills, cv_skills):
    jd_set = set(jd_skills) if isinstance(jd_skills, list) else set()
    cv_set = set(
        cv_skills.get("technical_skills", []) + cv_skills.get("soft_skills", [])
    )
    return list(jd_set - cv_set)
