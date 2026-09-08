"""
score_jobs.py

Scores each job description against the resume profile text using
TF-IDF + cosine similarity, and tags which explicit skills from the
resume appear in each job description.

Score is 0.0 (no overlap) to 1.0 (identical word-importance fingerprint).
In practice, well-matched postings usually land somewhere in the 0.15-0.45
range -- TF-IDF scores are relative, so what matters is the ranking, not
the raw number.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_matched_skills(job_description, skills):
    text = job_description.lower()
    matched = []
    for skill in skills:
        # word-boundary-ish match so "R" doesn't match inside "AWS" etc.
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text):
            matched.append(skill)
    return matched


def score_jobs(jobs, resume_profile):
    if not jobs:
        return []

    profile_text = resume_profile["profile_text"]
    skills = resume_profile["skills"]

    documents = [profile_text] + [job["description"] for job in jobs]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    scored_jobs = []
    for job, sim in zip(jobs, similarities):
        job_copy = dict(job)
        job_copy["score"] = round(float(sim), 4)
        job_copy["matched_skills"] = find_matched_skills(job["description"], skills)
        scored_jobs.append(job_copy)

    scored_jobs.sort(key=lambda j: j["score"], reverse=True)
    return scored_jobs
