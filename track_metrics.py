import os
import requests
import csv
from datetime import datetime

TOKEN = os.getenv("GH_TOKEN")
REPO = "yvsoucom/yvsou-cms"  # ← Change this
HEADERS = {"Authorization": f"token {TOKEN}"}
BASE = "https://api.github.com/repos/" + REPO

def fetch_json(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def append_csv(file, fieldnames, row):
    exists = os.path.exists(file)
    with open(file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)

today = datetime.utcnow().strftime("%Y-%m-%d")

# Clone stats
clones = fetch_json(BASE + "/traffic/clones")
append_csv("metrics/clone-stats.csv", ["date", "clones", "unique_cloners"], {
    "date": today,
    "clones": clones["count"],
    "unique_cloners": clones["uniques"]
})

# Repo stats
repo = fetch_json(BASE)
append_csv("metrics/repo-stats.csv", ["date", "stars", "forks", "watchers"], {
    "date": today,
    "stars": repo["stargazers_count"],
    "forks": repo["forks_count"],
    "watchers": repo["subscribers_count"]
})
