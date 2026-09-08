"""
main.py

Entry point run daily by GitHub Actions. Loads config + resume profile,
fetches fresh jobs, scores them, and rebuilds the dashboard HTML.
"""

import json
import yaml

from scripts.fetch_jobs import fetch_all_jobs
from scripts.score_jobs import score_jobs
from scripts.build_dashboard import build_dashboard


def main():
    with open("config.yml") as f:
        config = yaml.safe_load(f)

    with open("data/resume_profile.json") as f:
        resume_profile = json.load(f)

    print("Fetching jobs...")
    jobs = fetch_all_jobs(config)
    print(f"Fetched {len(jobs)} unique jobs.")

    print("Scoring jobs against resume...")
    scored = score_jobs(jobs, resume_profile)

    print("Building dashboard...")
    build_dashboard(scored, top_n=config["top_n_to_show"])

    print("Done.")


if __name__ == "__main__":
    main()
