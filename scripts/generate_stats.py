#!/usr/bin/env python3
"""Generate self-hosted GitHub profile stat cards as static SVGs.

Why this exists: public github-readme-stats instances (vercel demo) get
rate-limited / paused, which breaks profile images. This script queries the
GitHub API directly and commits deterministic SVGs into the repo, so the
profile README always displays. Refreshed weekly by
.github/workflows/update-stats.yml.

Outputs:
  assets/stats.svg      -- stars / commits / PRs / issues / followers / repos
  assets/top-langs.svg  -- language bytes across public non-fork repos

Stdlib only (urllib). Token: env GITHUB_TOKEN (or GH_TOKEN).
"""

import json
import os
import sys
import urllib.request

USER = os.environ.get("STATS_USER", "aifeifei798")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OUT_DIR = os.environ.get("OUT_DIR", "assets")

API = "https://api.github.com"


def api(path, params=""):
    url = f"{API}{path}" + (f"?{params}" if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-stats-gen",
    })
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query):
    req = urllib.request.Request(
        f"{API}/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "profile-stats-gen",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL errors: {data['errors']}")
    return data["data"]


def collect_stats():
    user = api(f"/users/{USER}")
    stats = {
        "followers": user["followers"],
        "repos": user["public_repos"],
    }

    # stars over owned public repos (paginate, ignore forks)
    stars = 0
    page = 1
    repo_names = []
    while True:
        repos = api(f"/users/{USER}/repos", f"type=owner&per_page=100&page={page}")
        if not repos:
            break
        for r in repos:
            if r.get("fork"):
                continue
            stars += r["stargazers_count"]
            repo_names.append(r["full_name"])
        page += 1
    stats["stars"] = stars
    stats["source_repos"] = repo_names

    g = graphql(f'''query {{
  user(login: "{USER}") {{
    contributionsCollection {{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
    }}
  }}
}}''')
    c = g["user"]["contributionsCollection"]
    stats["commits_1y"] = c["totalCommitContributions"]
    stats["prs_1y"] = c["totalPullRequestContributions"]
    stats["issues_1y"] = c["totalIssueContributions"]
    return stats


# GitHub language colors (github-readme-stats palette); hashed fallback for others
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "C++": "#f34b7d", "C": "#555555", "Cuda": "#6E4C13", "HTML": "#e34c26",
    "CSS": "#563d7c", "SCSS": "#c6538c", "Shell": "#89e051", "Jinja": "#a52a22",
    "Vue": "#41b883", "Go": "#00ADD8", "Rust": "#dea584", "Nunjucks": "#3d8137",
    "Svelte": "#ff3e00", "Dockerfile": "#384d54", "PowerShell": "#012456",
    "Lua": "#000080", "Makefile": "#427819", "Cython": "#fedf5b", "Nix": "#7e7eff",
    "Perl": "#0298c3", "R": "#198CE7", "Markdown": "#083fa1", "Astro": "#ff5a03",
    "Starlark": "#00d3b8", "Less": "#1d365d", "CoffeeScript": "#244776",
}


def color_for(name):
    if name in LANG_COLORS:
        return LANG_COLORS[name]
    h = sum(ord(ch) * (i + 7) for i, ch in enumerate(name))
    palette = ["#41b883", "#00ADD8", "#a371f7", "#f34b7d", "#e38c00", "#2ea44f"]
    return palette[h % len(palette)]


def collect_languages(repo_names, max_langs=8):
    totals = {}
    for full in repo_names:
        langs = api(f"/repos/{full}/languages")
        for lang, b in langs.items():
            totals[lang] = totals.get(lang, 0) + b
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    total = sum(totals.values()) or 1
    top = ranked[:max_langs]
    other = total - sum(b for _, b in top)
    result = [(name, b / total * 100) for name, b in top if b / total >= 0.001]
    if other / total >= 0.005:
        result.append(("Other", other / total * 100))
    return result


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt(n):
    return f"{n:,}"


BG, BORDER, TXT, MUTED = "#0d1117", "#30363d", "#c9d1d9", "#8b949e"
FONT = 'font-family="Segoe UI, Ubuntu, DejaVu Sans, Helvetica, Arial, sans-serif"'


def stats_svg(s):
    w, h = 420, 165
    cells = [
        ("Total Stars", fmt(s["stars"])), ("Total Commits (1y)", fmt(s["commits_1y"])),
        ("Total PRs (1y)", fmt(s["prs_1y"])), ("Total Issues (1y)", fmt(s["issues_1y"])),
        ("Followers", fmt(s["followers"])), ("Public Repos", fmt(s["repos"])),
    ]
    x0, y0, cw, rh = 32, 42, 190, 36
    body = []
    for i, (label, val) in enumerate(cells):
        cx = x0 + (i % 2) * cw
        cy = y0 + (i // 2) * rh
        body.append(f'<text x="{cx}" y="{cy}" font-size="11" fill="{MUTED}" {FONT}>{esc(label)}</text>')
        body.append(f'<text x="{cx}" y="{cy + 20}" font-size="18" font-weight="600" fill="{TXT}" {FONT}>{esc(val)}</text>')
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4.5" fill="{BG}" stroke="{BORDER}"/>
{''.join(body)}
</svg>
'''


def langs_svg(langs):
    w, h = 420, 160
    pad = 32
    bar_w, bar_h = w - 2 * pad, 8
    parts = []
    x = pad
    for name, pct in langs:
        seg = bar_w * pct / 100
        parts.append(f'<rect x="{x:.1f}" y="36" width="{seg:.1f}" height="{bar_h}" rx="2" fill="{color_for(name)}"/>')
        x += seg
    body = []
    col_w = (w - 2 * pad) / 2
    for i, (name, pct) in enumerate(langs):
        cx = pad + (i % 2) * col_w
        cy = 66 + (i // 2) * 24
        body.append(f'<circle cx="{cx + 4}" cy="{cy - 4}" r="5" fill="{color_for(name)}"/>')
        body.append(f'<text x="{cx + 14}" y="{cy}" font-size="12" fill="{TXT}" {FONT}>{esc(name)}</text>')
        body.append(f'<text x="{cx + col_w - 12}" y="{cy}" font-size="12" fill="{MUTED}" text-anchor="end" {FONT}>{pct:.1f}%</text>')
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4.5" fill="{BG}" stroke="{BORDER}"/>
{''.join(parts)}
{''.join(body)}
</svg>
'''


def main():
    if not TOKEN:
        raise SystemExit("Set GITHUB_TOKEN (or GH_TOKEN)")
    s = collect_stats()
    langs = collect_languages(s["source_repos"])
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f"{OUT_DIR}/stats.svg", "w") as f:
        f.write(stats_svg(s))
    with open(f"{OUT_DIR}/top-langs.svg", "w") as f:
        f.write(langs_svg(langs))
    print("stats:", {k: v for k, v in s.items() if k != "source_repos"})
    print("languages:")
    for name, pct in langs:
        print(f"  {name:<14} {pct:5.1f}%  {color_for(name)}")
    print(f"wrote {OUT_DIR}/stats.svg, {OUT_DIR}/top-langs.svg")


if __name__ == "__main__":
    main()
