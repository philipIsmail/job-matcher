"""
build_dashboard.py

Renders the top-N scored jobs into a single static HTML page at docs/index.html.
GitHub Pages serves whatever is in /docs on the main branch, so overwriting
this file and pushing it is enough to update the live dashboard.
"""

from datetime import datetime, timezone
from jinja2 import Template

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Daily Job Matches</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; max-width: 900px;
         margin: 40px auto; padding: 0 20px; background: #fafafa; color: #1a1a1a; }
  h1 { font-size: 1.6rem; margin-bottom: 0; }
  .updated { color: #666; font-size: 0.9rem; margin-bottom: 30px; }
  .job { background: white; border: 1px solid #e0e0e0; border-radius: 10px;
         padding: 18px 20px; margin-bottom: 14px; }
  .job-title { font-size: 1.1rem; font-weight: 600; margin: 0 0 4px 0; }
  .job-title a { color: #1a1a1a; text-decoration: none; }
  .job-title a:hover { text-decoration: underline; }
  .job-meta { color: #555; font-size: 0.92rem; margin-bottom: 8px; }
  .score { display: inline-block; background: #eef4ff; color: #1a4dab;
           border-radius: 6px; padding: 2px 8px; font-size: 0.85rem; font-weight: 600; }
  .skills { margin-top: 8px; }
  .skill-tag { display: inline-block; background: #f0f0f0; border-radius: 5px;
               padding: 2px 7px; margin: 2px 3px 0 0; font-size: 0.8rem; color: #333; }
  .empty { color: #777; }
</style>
</head>
<body>
  <h1>Daily Job Matches</h1>
  <div class="updated">Last updated: {{ updated }} UTC · {{ count }} jobs ranked</div>

  {% if jobs %}
    {% for job in jobs %}
    <div class="job">
      <div class="job-title"><a href="{{ job.url }}" target="_blank">{{ job.title }}</a></div>
      <div class="job-meta">{{ job.company }} &middot; {{ job.location }}
        &middot; <span class="score">match {{ (job.score * 100) | round(1) }}%</span>
      </div>
      {% if job.matched_skills %}
      <div class="skills">
        {% for skill in job.matched_skills %}
        <span class="skill-tag">{{ skill }}</span>
        {% endfor %}
      </div>
      {% endif %}
    </div>
    {% endfor %}
  {% else %}
    <p class="empty">No jobs found today.</p>
  {% endif %}
</body>
</html>
"""


def build_dashboard(scored_jobs, top_n, output_path="docs/index.html"):
    top_jobs = scored_jobs[:top_n]
    html = Template(TEMPLATE).render(
        jobs=top_jobs,
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        count=len(top_jobs),
    )
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Wrote dashboard with {len(top_jobs)} jobs to {output_path}")
