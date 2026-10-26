"""Rewrites the activity section of README.md from the user's public GitHub events."""
import json
import os
import re
import urllib.request
from datetime import datetime

USER = os.environ.get("GH_USER", "Louay-El-hajj")
MAX_LINES = int(os.environ.get("MAX_LINES", "6"))
README = "README.md"


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def link(repo):
    return f"[{repo.split('/')[-1]}](https://github.com/{repo})"


def describe(e):
    repo, p, t = e["repo"]["name"], e.get("payload", {}), e["type"]
    if t == "PushEvent":
        n = p.get("size") or len(p.get("commits", [])) or 1
        return f"🚀 Pushed {n} commit{'s' if n != 1 else ''} to {link(repo)}"
    if t == "CreateEvent" and p.get("ref_type") == "repository":
        return f"🌱 Created repository {link(repo)}"
    if t == "CreateEvent" and p.get("ref_type") == "branch":
        return f"🌿 Created branch `{p.get('ref')}` in {link(repo)}"
    if t == "PullRequestEvent":
        pr = p["pull_request"]
        verb = "Merged" if pr.get("merged") else p.get("action", "updated").capitalize()
        return f"🔀 {verb} PR [#{pr['number']}]({pr['html_url']}) in {link(repo)}"
    if t == "IssuesEvent":
        i = p["issue"]
        return f"🐞 {p.get('action', 'updated').capitalize()} issue [#{i['number']}]({i['html_url']}) in {link(repo)}"
    if t == "IssueCommentEvent":
        i = p["issue"]
        return f"💬 Commented on [#{i['number']}]({p['comment']['html_url']}) in {link(repo)}"
    if t == "ReleaseEvent":
        r = p["release"]
        return f"🏷️ Released [{r.get('tag_name')}]({r['html_url']}) in {link(repo)}"
    if t == "WatchEvent":
        return f"⭐ Starred {link(repo)}"
    if t == "ForkEvent":
        return f"🍴 Forked {link(repo)}"
    return None


def main():
    lines, seen = [], set()
    for e in api(f"users/{USER}/events/public?per_page=100"):
        text = describe(e)
        if not text:
            continue
        key = (e["type"], e["repo"]["name"], e["created_at"][:10])
        if key in seen:
            continue
        seen.add(key)
        day = datetime.strptime(e["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d")
        lines.append(f"{len(lines) + 1}. {text} <sub>· {day}</sub>")
        if len(lines) == MAX_LINES:
            break
    if not lines:  # quiet period: fall back to most recently pushed repos
        for r in api(f"users/{USER}/repos?sort=pushed&per_page={MAX_LINES}"):
            day = datetime.strptime(r["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
            lines.append(f"{len(lines) + 1}. 🛠️ Worked on {link(r['full_name'])} <sub>· {day}</sub>")

    readme = open(README, encoding="utf-8").read()
    new = re.sub(
        r"(<!--START_SECTION:activity-->).*?(<!--END_SECTION:activity-->)",
        lambda m: m.group(1) + "\n" + "\n".join(lines) + "\n" + m.group(2),
        readme,
        flags=re.S,
    )
    if new != readme:
        open(README, "w", encoding="utf-8", newline="\n").write(new)
        print("README updated")
    else:
        print("No change")


if __name__ == "__main__":
    main()
