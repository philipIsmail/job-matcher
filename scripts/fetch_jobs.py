"""
fetch_jobs.py

Pulls job listings from the Adzuna API for each search term in config.yml,
de-duplicates them, and returns a flat list of job dicts.

Adzuna credentials are read from environment variables (ADZUNA_APP_ID,
ADZUNA_APP_KEY) so they never live in the code or the repo itself.
"""

import os
import time
import requests

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/1"


def fetch_jobs_for_term(term, country_code, app_id, app_key, results_per_page):
    """Fetch one page of results for a single search term."""
    url = ADZUNA_BASE_URL.format(country=country_code)
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": term,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])


def fetch_all_jobs(config):
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise EnvironmentError(
            "Missing ADZUNA_APP_ID / ADZUNA_APP_KEY environment variables. "
            "Set these as GitHub Actions secrets (see README)."
        )

    all_jobs = {}  # keyed by job id to de-duplicate across search terms

    for term in config["search_terms"]:
        try:
            results = fetch_jobs_for_term(
                term=term,
                country_code=config["country_code"],
                app_id=app_id,
                app_key=app_key,
                results_per_page=config["results_per_search_term"],
            )
        except requests.HTTPError as e:
            print(f"[warn] search term '{term}' failed: {e}")
            continue

        for job in results:
            job_id = job.get("id")
            if job_id and job_id not in all_jobs:
                all_jobs[job_id] = {
                    "id": job_id,
                    "title": job.get("title", "").strip(),
                    "company": (job.get("company") or {}).get("display_name", "Unknown"),
                    "location": (job.get("location") or {}).get("display_name", "Unknown"),
                    "description": job.get("description", ""),
                    "url": job.get("redirect_url", ""),
                    "created": job.get("created", ""),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                }

        time.sleep(1)  # be polite to the free-tier rate limit

    return list(all_jobs.values())


if __name__ == "__main__":
    import yaml
    with open("config.yml") as f:
        cfg = yaml.safe_load(f)
    jobs = fetch_all_jobs(cfg)
    print(f"Fetched {len(jobs)} unique jobs.")
