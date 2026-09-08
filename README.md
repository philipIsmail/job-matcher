# Daily Job Matcher

Pulls fresh job listings every day, scores them against your resume, and
publishes a ranked dashboard as a webpage you can bookmark.

## How it works

1. `data/resume_profile.json` holds your resume, flattened into a skills list
   and a single block of text.
2. Every day, GitHub Actions runs `main.py`, which:
   - Fetches jobs from the [Adzuna API](https://developer.adzuna.com/) for
     the search terms in `config.yml`
   - Scores each posting against your resume using TF-IDF + cosine similarity
   - Tags which of your explicit skills appear in each posting
   - Rewrites `docs/index.html` with the top matches
3. GitHub Pages serves `docs/index.html` as a live page.

## One-time setup

### 1. Create the repo
Create a new **public** GitHub repo (Pages' free tier needs public, unless
you're on GitHub Pro/Team) and push this folder to it:

```bash
cd job-matcher
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

### 2. Add your Adzuna credentials as secrets
Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**,
and add two secrets:

- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`

(Get these free from https://developer.adzuna.com/ if you haven't already.)
Never put these values directly in `config.yml` or any script — secrets keep
them encrypted and out of the repo's visible history.

### 3. Turn on GitHub Pages
Repo → **Settings → Pages** → under "Build and deployment," set:
- Source: **Deploy from a branch**
- Branch: **main**, folder: **/docs**

Save. GitHub will give you a URL like
`https://<your-username>.github.io/<repo-name>/` — that's your dashboard.

### 4. Run it once manually
Repo → **Actions** tab → **Daily Job Match** workflow → **Run workflow**.
This does an immediate test run instead of waiting for the schedule, and
will fill in the dashboard for the first time.

## Customizing

- **Search terms / location / how many results**: edit `config.yml` — no
  code changes needed.
- **Resume content**: edit `data/resume_profile.json` any time your resume
  changes. Keep `skills` as a flat list and `profile_text` as one blob of
  plain text (bullets, skills, everything).
- **Schedule**: edit the `cron` line in `.github/workflows/daily.yml`
  ([crontab.guru](https://crontab.guru) helps write these). Times are UTC.
- **Add Greenhouse/Lever direct pulls later**: each company's board is a
  free public JSON endpoint, e.g.
  `https://boards-api.greenhouse.io/v1/boards/{company}/jobs`. A follow-up
  script can hit a list of these and merge results into the same pipeline —
  happy to build that whenever you have a target company list.

## Local testing (optional)

```bash
pip install -r requirements.txt
export ADZUNA_APP_ID=your_id
export ADZUNA_APP_KEY=your_key
python main.py
open docs/index.html   # or just open the file in a browser
```
